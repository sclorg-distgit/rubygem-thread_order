%{?scl:%scl_package rubygem-%{gem_name}}
%{!?scl:%global pkg_name %{name}}

%global	gem_name	thread_order

Name:		%{?scl_prefix}rubygem-%{gem_name}
Version:	1.1.0
Release:	3%{?dist}

Summary:	Test helper for ordering threaded code
License:	MIT
URL:		https://github.com/JoshCheek/thread_order
Source0:	https://rubygems.org/gems/%{gem_name}-%{version}.gem

Requires:       %{?scl_prefix_ruby}ruby(rubygems)
BuildRequires:	%{?scl_prefix_ruby}ruby(release)
BuildRequires:	%{?scl_prefix_ruby}rubygems-devel
BuildRequires:	%{?scl_prefix}rubygem(rspec) >= 3
BuildArch:	    noarch
Provides:       %{?scl_prefix}rubygem(%{gem_name}) = %{version}

%description
Test helper for ordering threaded code.

%package	doc
Summary:	Documentation for %{pkg_name}
Group:	Documentation
Requires:	%{?scl_prefix}%{pkg_name} = %{version}-%{release}
BuildArch:	noarch

%description doc
Documentation for %{pkg_name}.

%prep
%{?scl:scl enable %{scl} - << \EOF}
gem unpack %{SOURCE0}
%{?scl:EOF}
%setup -q -D -T -n %{gem_name}-%{version}
%{?scl:scl enable %{scl} - << \EOF}
gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec
%{?scl:EOF}


%build
%{?scl:scl enable %{scl} - << \EOF}
gem build %{gem_name}.gemspec
%gem_install
%{?scl:EOF}


%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
	%{buildroot}%{gem_dir}/

pushd %{buildroot}
rm -f .%{gem_cache}
popd

pushd .%{gem_instdir}
rm -rf \
	.gitignore .travis.yml \
	Gemfile \
	spec/ \
	%{gem_name}.gemspec \
	%{nil}

popd

%check
# The following test does not pass with using gem
FAILFILE=()
FAILTEST=()
FAILFILE+=("spec/thread_order_spec.rb")
FAILTEST+=("is implemented without depending on the stdlib")

#pushd .%{gem_instdir}
for ((i = 0; i < ${#FAILFILE[@]}; i++)) {
	sed -i \
		-e "\@${FAILTEST[$i]}@s|do$|, :broken => true do|" \
		${FAILFILE[$i]}
}

%{?scl:scl enable %{scl} - << \EOF}
rspec spec/ || \
	rspec spec/ --tag ~broken
%{?scl:EOF}
#popd

%files
%dir         %{gem_instdir}
%license     %{gem_instdir}/License.txt
%doc         %{gem_instdir}/Readme.md
%exclude     %{gem_instdir}/.*
%exclude     %{gem_instdir}/spec

%{gem_libdir}
%{gem_spec}

%files doc
%doc	     %{gem_docdir}
%{gem_instdir}/Gemfile
%{gem_instdir}/%{gem_name}.gemspec

%changelog
* Tue Feb 23 2016 Pavel Valena <pvalena@redhat.com> - 1.1.0-3
- Add scl macros

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sun Aug 09 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.1.0-1
- Initial package
