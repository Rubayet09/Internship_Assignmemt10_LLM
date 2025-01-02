import os
import json
import pytest
from unittest.mock import patch, MagicMock
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from projectscrape.main import setup_database, save_to_database, save_to_json, Property, TripComSpider
from scrapy.http import HtmlResponse, Request

@pytest.fixture(scope="module")
def test_database():
    """Set up a test database."""
    # Use test database URL from environment or fallback to SQLite
    test_db_url = os.getenv('DATABASE_URL', 'sqlite:///:memory:')
    engine = create_engine(test_db_url)
    Property.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()
    engine.dispose()

@pytest.fixture
def mock_json_file(tmp_path):
    """Create a temporary JSON file for testing."""
    test_json_file = tmp_path / "test_hotels.json"
    return str(test_json_file)

@pytest.fixture
def mock_session():
    """Create a mock database session."""
    return MagicMock()

def test_save_to_database(test_database):
    """Test saving a property to the database."""
    test_data = {
        "title": "Test Hotel",
        "rating": 4.5,
        "location": "Test City",
        "latitude": 12.3456,
        "longitude": 78.9012,
        "room_type": "Deluxe Room",
        "price": 123.45,
        "image_path": "path/to/image.jpg"
    }

    # Clear database before running the test
    test_database.query(Property).delete()
    test_database.commit()

    save_to_database(test_data, test_database)

    # Check if the property was added
    result = test_database.query(Property).first()
    assert result is not None
    assert result.title == "Test Hotel"
    assert result.rating == 4.5
    assert result.location == "Test City"

def test_save_to_json(mock_json_file):
    """Test saving hotel data to a JSON file."""
    test_data = {
        "title": "Test Hotel JSON",
        "rating": 4.2,
        "location": "Test JSON Location"
    }
    save_to_json(test_data, mock_json_file)

    with open(mock_json_file, 'r') as f:
        content = f.readlines()
    assert len(content) == 1
    saved_data = json.loads(content[0])
    assert saved_data["title"] == "Test Hotel JSON"
    assert saved_data["rating"] == 4.2
    assert saved_data["location"] == "Test JSON Location"

def test_tripcom_spider_parse(mock_session, mock_json_file):
    """Test the initial parse method of TripComSpider."""
    spider = TripComSpider(session=mock_session, json_file=mock_json_file)
    
    html_content = """
    <html>
        <script>
            window.IBU_HOTEL = {
                "initData": {
                    "htlsData": {
                        "inboundCities": [
                            {"name": "City 1", "id": "101"},
                            {"name": "City 2", "id": "102"}
                        ],
                        "outboundCities": [
                            {"name": "City 3", "id": "103"}
                        ]
                    }
                }
            };
        </script>
    </html>
    """
    
    response = HtmlResponse(
        url="https://uk.trip.com/hotels/",
        body=html_content.encode('utf-8'),
        encoding='utf-8'
    )

    # Get generator results
    results = list(spider.parse(response))

    # Verify we got requests for 3 cities
    assert len(results) == 3
    assert all(isinstance(r, Request) for r in results)
    assert all('city_name' in r.meta for r in results)
    assert all('city_id' in r.meta for r in results)

def test_tripcom_spider_parse_city_hotels(mock_session, mock_json_file):
    """Test parsing city hotels logic."""
    spider = TripComSpider(session=mock_session, json_file=mock_json_file)
    
    html_content = """
    <html>
        <script>
            window.IBU_HOTEL = {
                "initData": {
                    "firstPageList": {
                        "hotelList": [
                            {
                                "hotelBasicInfo": {
                                    "hotelId": "123",
                                    "hotelName": "Test Hotel 1",
                                    "hotelImg": "http://example.com/img1.jpg",
                                    "price": 100
                                },
                                "positionInfo": {
                                    "positionName": "Test Location",
                                    "coordinate": {"lat": 10.0, "lng": 20.0}
                                },
                                "commentInfo": {"commentScore": 4.5},
                                "roomInfo": {"physicalRoomName": "Deluxe"}
                            }
                        ]
                    },
                    "pagination": {"nextPage": null}
                }
            };
        </script>
    </html>
    """
    
    response = HtmlResponse(
        url="https://uk.trip.com/hotels/list",
        body=html_content.encode('utf-8'),
        encoding='utf-8',
        meta={'city_name': 'Test City', 'city_id': '123', 'page': 1}
    )

    list(spider.parse_city_hotels(response))

    # Verify data was saved
    with open(mock_json_file, 'r') as f:
        content = f.readlines()
    
    assert len(content) == 1
    saved_data = json.loads(content[0])
    assert saved_data["title"] == "Test Hotel 1"
    assert saved_data["rating"] == 4.5
    assert saved_data["location"] == "Test Location"

if __name__ == "__main__":
    pytest.main(["--cov=projectscrape", "--cov-report=term-missing"])