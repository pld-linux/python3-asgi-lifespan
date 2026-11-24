#
# Conditional build:
%bcond_without	tests	# unit tests

%define		module	asgi_lifespan
Summary:	Programmatic startup/shutdown of ASGI apps
Summary(pl.UTF-8):	Programowe uruchamianie i zatrzymywanie aplikacji ASGI
Name:		python3-asgi-lifespan
Version:	2.1.0
Release:	1
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/asgi-lifespan/
Source0:	https://files.pythonhosted.org/packages/source/a/asgi-lifespan/asgi-lifespan-%{version}.tar.gz
# Source0-md5:	012663870ff5ccc3f222e3f5cd61c550
URL:		https://github.com/florimondmanca/asgi-lifespan
BuildRequires:	python3-build
BuildRequires:	python3-installer
BuildRequires:	python3-modules >= 1:3.7
BuildRequires:	python3-setuptools
BuildRequires:	python3-setuptools_scm
BuildRequires:	python3-wheel
%if %{with tests}
BuildRequires:	python3-httpx
BuildRequires:	python3-pytest
BuildRequires:	python3-pytest-asyncio
BuildRequires:	python3-sniffio
BuildRequires:	python3-starlette
BuildRequires:	python3-trio
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 2.044
Requires:	python3-modules >= 1:3.7
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Programmatically send startup/shutdown lifespan events into ASGI
applications. When mocking out the ASGI server, this allows to run
the application lifespan handlers, e.g. in tests.

%description -l pl.UTF-8
Programowe wysyłanie zdarzeń cyklu życia (startup/shutdown) do
aplikacji ASGI. Pozwala to uruchomić procedury obsługi cyklu życia
aplikacji bez serwera ASGI, np. w testach.

%prep
%setup -q -n asgi-lifespan-%{version}

%build
%py3_build_pyproject

%if %{with tests}
# trio tests: with trio >= 0.25 strict exception groups the trio backend
# raises ExceptionGroup instead of the app's exception (no upstream fix);
# test_lifespan_state_async_cm uses AsyncClient(app=) removed in httpx 0.28
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS=pytest_asyncio.plugin \
PYTHONPATH=$(pwd)/src \
%{__python3} -m pytest -o addopts= tests \
	-k 'not trio and not test_lifespan_state_async_cm'
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install_pyproject

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGELOG.md LICENSE README.md
%{py3_sitescriptdir}/asgi_lifespan
%{py3_sitescriptdir}/asgi_lifespan-%{version}.dist-info
