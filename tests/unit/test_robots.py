from svgai_marketing.crawler.robots import parse_robots


def test_parses_groups_sitemaps_and_crawl_delay() -> None:
    groups, sitemaps = parse_robots(
        """
        User-agent: *
        Allow: /public/
        Disallow: /private/
        Crawl-delay: 2.5
        Sitemap: https://example.test/sitemap.xml

        User-agent: ExampleBot
        Disallow: /
        """
    )

    assert sitemaps == ["https://example.test/sitemap.xml"]
    assert groups[0] == {
        "user_agents": ["*"],
        "allow": ["/public/"],
        "disallow": ["/private/"],
        "crawl_delay": 2.5,
    }
    assert groups[1]["user_agents"] == ["examplebot"]


def test_ignores_comments_and_invalid_delay() -> None:
    groups, _ = parse_robots("User-agent: * # all\nCrawl-delay: soon\nDisallow:\n")
    assert groups[0]["crawl_delay"] is None
    assert groups[0]["disallow"] == [""]
