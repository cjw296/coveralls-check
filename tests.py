import pytest
from coveralls_check import main
from mock import Mock
from responses import RequestsMock
from testfixtures import replace, ShouldRaise, OutputCapture, Replacer, compare

SAMPLE_JSON = {
    "commit_sha": "xyz",
    "coverage_change": 0,
    "covered_percent": 99.38
}


@pytest.fixture(autouse=True)
def responses():
    with RequestsMock() as responses:
        yield responses


@pytest.fixture(autouse=True)
def mocks():
    with Replacer() as r:
        m = Mock()
        m.argv = ['script.py', 'xyz']
        r.replace('sys.argv', m.argv)
        yield m


def test_ok(responses, mocks):
    mocks.argv.extend(['--fail-under', '99'])
    responses.add(responses.GET, 'https://coveralls.io/builds/xyz.json',
                  json=SAMPLE_JSON)
    with OutputCapture() as output:
        main()
    output.compare('Coverage OK for xyz as 99.38 >= 99.0')


def test_not_ok(responses):
    responses.add(responses.GET, 'https://coveralls.io/builds/xyz.json',
                  json=SAMPLE_JSON)
    with ShouldRaise(SystemExit(2)):
        with OutputCapture() as output:
            main()
    output.compare('Failed coverage check for xyz as 99.38 < 100')


def test_coveralls_returns_none(responses):
    responses.add(responses.GET, 'https://coveralls.io/builds/xyz.json',
                  json={"covered_percent": None})
    with ShouldRaise(SystemExit(1)):
        with OutputCapture() as output:
            main()
    output.compare('No coverage information available')
