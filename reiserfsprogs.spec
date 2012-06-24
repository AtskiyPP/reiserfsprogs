Summary:	Utilities belonging to the Reiser filesystem
Summary(pl):	Narz�dzia dla systemu plik�w Reiser
Name:		reiserfsprogs
Version:	3.x.0j
Release:	1
Copyright:	2001 Hans Reiser
Group:		Applications/System
Group(de):	Applikationen/System
Group(pl):	Aplikacje/System
Source0:	ftp://ftp.reiserfs.org/pub/reiserfsprogs/%{name}-%{version}.tar.gz
URL:		http://www.reiserfs.org/
Obsoletes:	reiserfs-utils
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
%if %{?BOOT:1}%{!?BOOT:0}
BuildRequires:	glibc-static
%endif

%define		_sbindir	/sbin

%description
The reiserfsprogs package contains programs for creating (mkreiserfs),
checking and correcting any inconsistencies (reiserfsck) and resizing
(resize_reiserfs) of a reiserfs filesystem.

%description -l pl
Pakiet zawiera programy do tworzenia (mkreiserfs), sprawdzania i
naprawiania b��d�w (reiserfsck) oraz zmiany wielko�ci
(resize_reiserfs) systemu plik�w ReiserFS.

%if %{?BOOT:1}%{!?BOOT:0}
%package BOOT
Summary:	%{name} for bootdisk
Group:		Applications/System
%description BOOT
%endif

%prep
%setup -q

%build

%if %{?BOOT:1}%{!?BOOT:0}
%configure
%{__make} LDFLAGS="-static -s"
mv -f mkreiserfs/mkreiserfs mkreiserfs-BOOT
%{__make} distclean
%endif

%configure
%{__make} all

%install
rm -rf $RPM_BUILD_ROOT

%if %{?BOOT:1}%{!?BOOT:0}
install -d $RPM_BUILD_ROOT/usr/lib/bootdisk/sbin
for i in *-BOOT; do 
  install $i $RPM_BUILD_ROOT/usr/lib/bootdisk/sbin/`basename $i -BOOT`
done
%endif

install -d $RPM_BUILD_ROOT{%{_sbindir},%{_mandir}/man8}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

ln $RPM_BUILD_ROOT%{_sbindir}/reiserfsck $RPM_BUILD_ROOT%{_sbindir}/fsck.reiserfs
ln $RPM_BUILD_ROOT%{_sbindir}/mkreiserfs $RPM_BUILD_ROOT%{_sbindir}/mkfs.reiserfs

gzip -9nf README

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.gz
%attr(755, root, root) %{_sbindir}
%{_mandir}/man*/*

%if %{?BOOT:1}%{!?BOOT:0}
%files BOOT
%defattr(644,root,root,755)
%attr(755,root,root) /usr/lib/bootdisk/sbin/*
%endif
