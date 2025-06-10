# tests/test_parser.py
from app.utils.parser import sync_extract_price


def test_extract_price_from_html():
    html = """
    <html>
        <body>
            <span class="price">199.99</span>
        </body>
    </html>
    """
    assert sync_extract_price(html) == 199.99


def test_extract_price_no_tag():
    html = "<html><body>Цена не найдена</body></html>"
    assert sync_extract_price(html) is None


def test_extract_price_invalid():
    html = """
    <html>
        <body>
            <span class="price">Не число</span>
        </body>
    </html>
    """
    assert sync_extract_price(html) is None
