Name:		HALO
Version:	0.0.1
Release:	1%{?dist}
Summary:	HALO is a cluster management system designed for managing Lustre HA and similar use cases.

License:	MIT
URL:		https://github.com/lanl/halo
Source0:	halo-0.0.1.tgz

BuildRequires: cargo
BuildRequires: rust
BuildRequires: capnproto
BuildRequires: systemd-rpm-macros

Requires: systemd

%description
HALO is a cluster management system designed for managing Lustre HA and similar
use cases. HALO was previously known as GoLustre, and only supported Lustre HA,
but now it can manage other cluster types.

LANL software release number: O4905

%prep
%autosetup -n %{name}-%{version}

%build
cargo build

%install
install -D -p -m 0755 target/debug/halo %{buildroot}%{_bindir}/halo
install -D -p -m 0755 target/debug/halo_remote %{buildroot}%{_bindir}/halo_remote
install -D -p -m 0755 target/debug/halo_manager %{buildroot}%{_bindir}/halo_manager

install -D -p -m 0644 systemd/halo.service %{buildroot}%{_unitdir}/halo.service
install -D -p -m 0644 systemd/halo-remote.service %{buildroot}%{_unitdir}/halo-remote.service

install -D -p -m 0644 docs/man/halo.1 %{buildroot}%{_mandir}/man1/halo.1
install -D -p -m 0644 docs/man/halo_manager.1 %{buildroot}%{_mandir}/man1/halo_manager.1
install -D -p -m 0644 docs/man/halo_remote.1 %{buildroot}%{_mandir}/man1/halo_remote.1

install -D -p -m 0644 sysconfig/halo %{buildroot}%{_sysconfdir}/sysconfig/halo

%check
cargo test || :

%files
%license LICENSE
%doc README.md
%{_bindir}/halo
%{_bindir}/halo_remote
%{_bindir}/halo_manager

%{_unitdir}/halo.service
%{_unitdir}/halo-remote.service

%{_mandir}/man1/halo.1*
%{_mandir}/man1/halo_manager.1*
%{_mandir}/man1/halo_remote.1*

%config(noreplace) %{_sysconfdir}/sysconfig/halo

%post
%systemd_post halo.service halo-remote.service

%preun
%systemd_preun halo.service halo-remote.service

%postun
%systemd_postun_with_restart halo.service halo-remote.service

%changelog
* Thu Jun 18 2026 Olaf Faaland <faaland1@llnl.gov> - 0.0.1-1
- Initial package
