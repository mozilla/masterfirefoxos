import requests
import pytest


acceptance = pytest.mark.acceptance


def assert_ok(url):
    response = requests.get(url)
    assert response.status_code == 200, '{} for {}'.format(
        response.status_code, url)


def get_all_versions(base_urls, slug):
    for url in base_urls:
        assert_ok('{}{}/'.format(url, slug))


@acceptance
def test_home_pages(base_urls):
    for url in base_urls:
        assert_ok(url)


@acceptance
def test_introduction(base_urls):
    get_all_versions(base_urls, 'introduction')


@acceptance
def test_demo_tips(base_urls):
    get_all_versions(base_urls, 'demo-tips')


@acceptance
def test_customer_guide(base_urls):
    get_all_versions(base_urls, 'customer-guide')


@acceptance
def test_key_features(base_urls):
    get_all_versions(base_urls, 'key-features')


@acceptance
def test_faq(base_urls):
    get_all_versions(base_urls, 'frequently-asked-questions')


@acceptance
def test_about(base_urls):
    get_all_versions(base_urls, 'about')


@acceptance
def test_quiz(base_urls):
    get_all_versions(base_urls, 'take-the-challenge')


@acceptance
def test_which_version(base_urls):
    get_all_versions(base_urls, 'which-version')
