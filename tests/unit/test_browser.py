from proofline_marketing.crawler.browser import _is_allowed_browser_request


def test_browser_privacy_mode_allows_same_host_and_local_schemes() -> None:
    page = "https://www.example.test/store"

    assert _is_allowed_browser_request("https://www.example.test/app.js", page)
    assert _is_allowed_browser_request("data:text/plain,proofline", page)
    assert _is_allowed_browser_request("blob:https://www.example.test/id", page)


def test_browser_privacy_mode_blocks_third_party_and_non_web_requests() -> None:
    page = "https://www.example.test/store"

    assert not _is_allowed_browser_request("https://analytics.example/collect", page)
    assert not _is_allowed_browser_request("https://cdn.example.test/app.js", page)
    assert not _is_allowed_browser_request("file:///tmp/private", page)
