Name:           libglade-java
Version:        2.12.8
Release:        %mkrel 1
Epoch:          0
Summary:        Java bindings for libglade
License:        LGPL
Group:          Development/Java
URL:            http://java-gnome.sourceforge.net/
Source0:        http://fr2.rpmfind.net/linux/gnome.org/sources/libglade-java/2.12/libglade-java-%{version}.tar.bz2
Source1:        http://fr2.rpmfind.net/linux/gnome.org/sources/libglade-java/2.12/libglade-java-%{version}.changes
Source2:        http://fr2.rpmfind.net/linux/gnome.org/sources/libglade-java/2.12/libglade-java-%{version}.md5sum
Source3:        http://fr2.rpmfind.net/linux/gnome.org/sources/libglade-java/2.12/libglade-java-%{version}.news
Source4:        java-gnome-macros.tar.bz2        
Requires:       libglade2.0
Requires:       libgnome-java
Requires:       libgtk-java
BuildRequires:  gcc-java >= 0:4.1.1
BuildRequires:  java-devel >= 0:1.4.2
BuildRequires:  jpackage-utils
BuildRequires:  libglade2.0-devel
BuildRequires:  libgnome-java >= 0:2.12.7
BuildRequires:  libgtk-java >= 0:2.10.2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

%description
libglade-java is a language binding that allows developers to write
Java applications that use libglade.  It is part of Java-GNOME.

%package        devel
Summary:        Compressed Java source files for %{name}
Group:          Development/Java
Requires:       %{name} = %{epoch}:%{version}-%{release}

%description    devel
Compressed Java source for %{name}. This is useful if you are developing
applications with IDEs like Eclipse.

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

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc doc/api AUTHORS COPYING NEWS README
%{_libdir}/*so*
%{_libdir}/*la
%{_libdir}/pkgconfig/*
%{_javadir}/*.jar

%files devel
%defattr(-,root,root)
%{_javadir}/*.zip


