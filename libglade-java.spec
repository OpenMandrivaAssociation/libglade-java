Name:           libglade-java
Version:        2.12.8
Release:        %mkrel 6
Epoch:          0
Summary:        Java bindings for libglade
License:        LGPL
Group:          System/Libraries
URL:            http://java-gnome.sourceforge.net/
Source0:        http://fr2.rpmfind.net/linux/gnome.org/sources/libglade-java/2.12/libglade-java-%{version}.tar.bz2
Source1:        http://fr2.rpmfind.net/linux/gnome.org/sources/libglade-java/2.12/libglade-java-%{version}.changes
Source2:        http://fr2.rpmfind.net/linux/gnome.org/sources/libglade-java/2.12/libglade-java-%{version}.md5sum
Source3:        http://fr2.rpmfind.net/linux/gnome.org/sources/libglade-java/2.12/libglade-java-%{version}.news
Source4:        java-gnome-macros.tar.bz2        
BuildRequires:  java-gcj-compat-devel
BuildRequires:  java-devel >= 0:1.4.2
BuildRequires:  java-rpmbuild
BuildRequires:  libglade2.0-devel
BuildRequires:  libgnome-java-devel >= 0:2.12.7
BuildRequires:  libgtk-java-devel >= 0:2.10.2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

%description
libglade-java is a language binding that allows developers to write
Java applications that use libglade.  It is part of Java-GNOME.

%package        devel
Summary:        Development files for %{name}
Group:          Development/Java
Requires:       %{name} = %{epoch}:%{version}-%{release}
Conflicts:      libglade-java < 2.12.8-2

%description    devel
Development files for %{name}.

%prep
%setup -q
%setup -q -T -D -a 4
%{__aclocal} -I macros --force
%{__autoconf} --force
%{__automake} --copy --force-missing
%{__libtoolize} --copy --force

%build
export CLASSPATH=
export JAVA=%{java}
export JAVAC=%{javac}
export JAR=%{jar}
export JAVADOC=%{javadoc}
export GCJ=%{gcj}
export CPPFLAGS="-I%{java_home}/include -I%{java_home}/include/linux"
%{configure2_5x} --with-jardir=%{_javadir}
%{make}

# pack up the java source
jarversion=$(echo -n %{version} | cut -d . -f -2)
jarname=$(echo -n %{name} | cut -d - -f 1 | sed "s/lib//")
zipfile=$PWD/$jarname$jarversion-src-%{version}.zip
pushd src/java
%{_bindir}/zip -9 -r $zipfile $(find -name \*.java)
popd

%install
%{__rm} -rf %{buildroot}
%{makeinstall_std}
%{__rm} -rf %{buildroot}/%{name}-%{version}

# install the src.zip and make a sym link
jarversion=$(echo -n %{version} | cut -d . -f -2)
jarname=$(echo -n %{name} | cut -d - -f 1 | sed "s/lib//")
%{__install} -m 644 $jarname$jarversion-src-%{version}.zip $RPM_BUILD_ROOT%{_datadir}/java/
pushd %{buildroot}%{_javadir}
%{__ln_s} $jarname$jarversion-src-%{version}.zip $jarname$jarversion-src.zip
popd

%if %mdkversion < 200900
%post -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -p /sbin/ldconfig
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc AUTHORS COPYING NEWS README
%{_libdir}/libgladejava-*.so
%{_libdir}/libgladejni-*.so
%{_javadir}/*.jar

%files devel
%defattr(-,root,root)
%doc doc/api
%{_javadir}/*.zip
%{_libdir}/*la
%{_libdir}/pkgconfig/*
%{_libdir}/libgladejava.so
%{_libdir}/libgladejni.so
