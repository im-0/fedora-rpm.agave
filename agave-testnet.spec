%global agave_suffix testnet
%global agave_crossbeam_commit fd279d707025f0e60951e429bf778b4813d1b6bf
%global agave_tokio_commit 7cf47705faacf7bf0e43e4131a5377b3291fce21
%global agave_curve25519_dalek_commit b500cdc2a920cd5bff9e2dd974d7b97349d61464

%global agave_user   agave-%{agave_suffix}
%global agave_group  agave-%{agave_suffix}
%global agave_home   %{_sharedstatedir}/agave/%{agave_suffix}/
%global agave_log    %{_localstatedir}/log/agave/%{agave_suffix}/
%global agave_etc    %{_sysconfdir}/agave/%{agave_suffix}/

# See ${AGAVE_SRC}/rust-toolchain.toml or ${AGAVE_SRC}/ci/rust-version.sh
%global rust_version 1.78.0

# Used only on x86_64:
#
# Available CPUs and features: `llc -march=x86-64 -mattr=help`.
# x86-64-v3 (close to Haswell):
#   AVX, AVX2, BMI1, BMI2, F16C, FMA, LZCNT, MOVBE, XSAVE
%global validator_target_cpu x86-64-v3
%global validator_target_cpu_mtune generic
# x86-64:
#   CMOV, CMPXCHG8B, FPU, FXSR, MMX, FXSR, SCE, SSE, SSE2
%global base_target_cpu x86-64
%global base_target_cpu_mtune generic

Name:       agave-%{agave_suffix}
# git 3e7563cdad47a731b4243c3cf59a69c5fe607f07
Version:    2.0.8
Release:    1jito%{?dist}
Summary:    Solana/Agave blockchain software (%{agave_suffix} version)

License:    Apache-2.0
URL:        https://github.com/anza-xyz/agave/
Source0:    https://github.com/anza-xyz/agave/archive/v%{version}/agave-%{version}.tar.gz

# Contains agave-$VERSION/vendor/*.
#     $ cargo vendor
#     $ mkdir agave-X.Y.Z
#     $ mv vendor agave-X.Y.Z/
#     $ tar vcJf agave-X.Y.Z.cargo-vendor.tar.xz agave-X.Y.Z
Source1:    agave-%{version}.cargo-vendor.tar.xz

# Crossbeam patched by Agave developers.
# `cargo vendor` does not support this properly: https://github.com/rust-lang/cargo/issues/9172.
Source2:    https://github.com/anza-xyz/crossbeam/archive/%{agave_crossbeam_commit}/agave-crossbeam-%{agave_crossbeam_commit}.tar.gz

# Tokio patched by Agave developers.
# `cargo vendor` does not support this properly: https://github.com/rust-lang/cargo/issues/9172.
Source3:    https://github.com/anza-xyz/solana-tokio/archive/%{agave_tokio_commit}/solana-tokio-%{agave_tokio_commit}.tar.gz

# curve25519-dalek patched by Agave developers.
# `cargo vendor` does not support this properly: https://github.com/rust-lang/cargo/issues/9172.
Source4:    https://github.com/anza-xyz/curve25519-dalek/archive/%{agave_curve25519_dalek_commit}/curve25519-dalek-%{agave_curve25519_dalek_commit}.tar.gz

Source102:  config.toml
Source103:  activate
Source104:  agave-validator.service
Source105:  agave-validator
Source107:  agave-watchtower.service
Source108:  agave-watchtower
Source109:  agave-validator.logrotate

Source300:  https://static.rust-lang.org/dist/rust-%{rust_version}-x86_64-unknown-linux-gnu.tar.gz
Source301:  https://static.rust-lang.org/dist/rust-%{rust_version}-aarch64-unknown-linux-gnu.tar.gz

Patch1001: jito01.patch
Patch1002: jito02.patch
Patch1003: jito03.patch
Patch1004: jito04.patch
Patch1005: jito05.patch

Patch2002: 0002-Manually-vendor-the-patched-crossbeam.patch
Patch2003: 0003-Manually-vendor-the-patched-tokio.patch
Patch2004: 0004-Manually-vendor-the-patched-curve25519-dalek.patch

ExclusiveArch:  x86_64 aarch64

BuildRequires:  findutils
BuildRequires:  git
BuildRequires:  rust-packaging
BuildRequires:  systemd-rpm-macros
BuildRequires:  gcc
BuildRequires:  clang
BuildRequires:  make
BuildRequires:  pkgconf-pkg-config
BuildRequires:  protobuf-compiler >= 3.15.0
BuildRequires:  protobuf-devel >= 3.15.0

BuildRequires:  perl

# libudev-devel
BuildRequires:  systemd-devel


%description
Web-Scale Blockchain for fast, secure, scalable, decentralized apps and marketplaces.
Version for %{agave_suffix}.


%package common
Summary: Solana/Agave common files (%{agave_suffix} version)


%description common
Solana/Agave common files (%{agave_suffix} version).


%package cli
Summary: Solana/Agave RPC CLI (%{agave_suffix} version)
Requires: %{name}-common = %{version}-%{release}


%description cli
Solana/Agave RPC CLI (%{agave_suffix} version).


%package utils
Summary: Solana/Agave local utilities (%{agave_suffix} version)
Requires: %{name}-common = %{version}-%{release}


%description utils
Solana/Agave local utilities (%{agave_suffix} version).


%package deps
Summary: Solana/Agave dependency libraries (%{agave_suffix} version)


%description deps
Solana/Agave dependency libraries (%{agave_suffix} version).


%package daemons
Summary: Solana/Agave daemons (%{agave_suffix} version)
Requires: %{name}-common = %{version}-%{release}
Requires: %{name}-cli = %{version}-%{release}
Requires: %{name}-utils = %{version}-%{release}
Requires: %{name}-deps = %{version}-%{release}
%ifarch x86_64
Requires: agave-perf-libs-%{agave_suffix}
%endif
Requires: logrotate
Requires: zstd
Requires(pre): shadow-utils
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd


%description daemons
Solana/Agave daemons (%{agave_suffix} version).


%package bpf-utils
Summary: Solana/Agave BPF utilities (%{agave_suffix} version)
Requires: %{name}-common = %{version}-%{release}


%description bpf-utils
Solana/Agave BPF utilities (%{agave_suffix} version).


%package sbf-utils
Summary: Solana/Agave SBF utilities (%{agave_suffix} version)
Requires: %{name}-common = %{version}-%{release}


%description sbf-utils
Solana/Agave SBF utilities (%{agave_suffix} version).


%package tests
Summary: Solana/Agave tests and benchmarks (%{agave_suffix} version)
Requires: %{name}-common = %{version}-%{release}
Requires: %{name}-deps = %{version}-%{release}
%ifarch x86_64
Requires: agave-perf-libs-%{agave_suffix}
%endif


%description tests
Solana/Agave tests and benchmarks (%{agave_suffix} version).


%prep
%setup -q -D -T -b0 -n agave-%{version}
# We do not extract vendored sources here, check below.
%setup -q -D -T -b2 -n agave-%{version}
%setup -q -D -T -b3 -n agave-%{version}
%setup -q -D -T -b4 -n agave-%{version}

%ifarch x86_64
%setup -q -D -T -b300 -n agave-%{version}
%endif
%ifarch aarch64
%setup -q -D -T -b301 -n agave-%{version}
%endif
../rust-%{rust_version}-%{_arch}-unknown-linux-gnu/install.sh \
        --prefix=../rust \
        --disable-ldconfig

# Apply Jito patch.
git config --global user.email "rpmbuild@example.org"
git config --global user.name "rpmbuild"
git init
git add .
git commit -m "import"
git am %{PATCH1001}
git am %{PATCH1002}
git am %{PATCH1003}
git am %{PATCH1004}
git am %{PATCH1005}

# Extract vendored sources after applying Jito patch because it contains
# git modules.
%setup -q -D -T -b1 -n agave-%{version}

# Apply all other patches.
%patch -P 2002 -p1
ln -sv ../crossbeam-%{agave_crossbeam_commit} ./agave-crossbeam

%patch -P 2003 -p1
ln -sv ../solana-tokio-%{agave_tokio_commit} ./solana-tokio

%patch -P 2004 -p1
ln -sv ../curve25519-dalek-%{agave_curve25519_dalek_commit} ./curve25519-dalek

mkdir .cargo
cp %{SOURCE102} .cargo/config.toml

# Fix Fedora's shebang mangling errors:
#     *** ERROR: ./usr/src/debug/agave-testnet-1.10.0-1.fc35.x86_64/vendor/ascii/src/ascii_char.rs has shebang which doesn't start with '/' ([cfg_attr(rustfmt, rustfmt_skip)])
find . -type f -name "*.rs" -exec chmod 0644 "{}" ";"


%build
export PATH="$( pwd )/../rust/bin:${PATH}"

export PROTOC=/usr/bin/protoc
export PROTOC_INCLUDE=/usr/include

%ifarch x86_64
%global cpu_base_cflags -march=%{base_target_cpu} -mtune=%{base_target_cpu_mtune}
%global cpu_base_rustflags -Ctarget-cpu=%{base_target_cpu}
%global cpu_validator_cflags -march=%{validator_target_cpu} -mtune=%{validator_target_cpu_mtune} -mpclmul
%global cpu_validator_rustflags -Ctarget-cpu=%{validator_target_cpu}
%else
%global cpu_base_cflags %{nil}
%global cpu_base_rustflags %{nil}
%global cpu_validator_cflags %{nil}
%global cpu_validator_rustflags %{nil}
%endif

# Check https://pagure.io/fedora-rust/rust2rpm/blob/main/f/data/macros.rust for
# rust-specific variables.
export RUSTC_BOOTSTRAP=1

export CC=clang
export CXX=clang++

# First, build binaries optimized for generic baseline CPU.
export RUSTFLAGS='%{build_rustflags} -Copt-level=3 %{cpu_base_rustflags}'
export CFLAGS="-O3 %{cpu_base_cflags}"
export CXXFLAGS="-O3 %{cpu_base_cflags}"
export LDFLAGS="-O3 %{cpu_base_cflags}"
cargo build %{__cargo_common_opts} --release --frozen

mv target/release ./_release
cargo clean

%ifarch x86_64
# Second, build binaries optimized for newer CPUs with "fat" LTO.
echo "[profile.release]" >>Cargo.toml
echo "lto = \"fat\"" >>Cargo.toml
export RUSTFLAGS='%{build_rustflags} -Ccodegen-units=1 -Copt-level=3 %{cpu_validator_rustflags}'
export CFLAGS="-O3 %{cpu_validator_cflags}"
export CXXFLAGS="-O3 %{cpu_validator_cflags}"
export LDFLAGS="-O3 %{cpu_validator_cflags}"
cargo build %{__cargo_common_opts} --release --frozen \
        --package agave-validator \
        --package solana-accounts-bench \
        --package solana-banking-bench \
        --package solana-bench-streamer \
        --package solana-merkle-root-bench \
        --package solana-poh-bench \
        --package solana-program:%{version}

mv target/release ./_release.optimized
cargo clean
%endif

sed 's,__SUFFIX__,%{agave_suffix},g' \
        <%{SOURCE103} \
        >activate
sed 's,__SUFFIX__,%{agave_suffix},g' \
        <%{SOURCE104} \
        >agave-validator.service
sed 's,__SUFFIX__,%{agave_suffix},g' \
        <%{SOURCE105} \
        >agave-validator
sed 's,__SUFFIX__,%{agave_suffix},g' \
        <%{SOURCE107} \
        >agave-watchtower.service
sed 's,__SUFFIX__,%{agave_suffix},g' \
        <%{SOURCE108} \
        >agave-watchtower
sed 's,__SUFFIX__,%{agave_suffix},g' \
        <%{SOURCE109} \
        >agave-validator.logrotate

./_release/solana completion --shell bash >solana.bash-completion


%install
mkdir -p %{buildroot}/opt/agave/%{agave_suffix}/bin/deps
mkdir -p %{buildroot}/opt/agave/%{agave_suffix}/bin/perf-libs
mkdir -p %{buildroot}/%{_unitdir}
mkdir -p %{buildroot}%{agave_home}
mkdir -p %{buildroot}%{agave_log}
mkdir -p %{buildroot}%{agave_etc}
mkdir -p %{buildroot}%{_sysconfdir}/sysconfig
mkdir -p %{buildroot}%{_sysconfdir}/logrotate.d

mv activate \
        %{buildroot}/opt/agave/%{agave_suffix}/
mv agave-validator.service \
        %{buildroot}/%{_unitdir}/agave-validator-%{agave_suffix}.service
mv agave-validator \
        %{buildroot}%{_sysconfdir}/sysconfig/agave-validator-%{agave_suffix}
mv agave-watchtower.service \
        %{buildroot}/%{_unitdir}/agave-watchtower-%{agave_suffix}.service
mv agave-watchtower \
        %{buildroot}%{_sysconfdir}/sysconfig/agave-watchtower-%{agave_suffix}
mv agave-validator.logrotate \
        %{buildroot}%{_sysconfdir}/logrotate.d/agave-validator-%{agave_suffix}

%ifarch x86_64
# Use binaries optimized for newer CPUs for running validator and local benchmarks.
mv _release.optimized/*.so ./_release/
mv _release.optimized/agave-validator ./_release/
mv _release.optimized/solana-accounts-bench ./_release/
mv _release.optimized/solana-banking-bench ./_release/
mv _release.optimized/solana-bench-streamer ./_release/
mv _release.optimized/solana-merkle-root-bench ./_release/
mv _release.optimized/solana-poh-bench ./_release/
mv _release.optimized/solana-test-validator ./_release/
%endif

find ./_release/ -mindepth 1 -maxdepth 1 -type d -exec rm -r "{}" \;
rm ./_release/*.d
rm ./_release/*.rlib
# Excluded because we do not need installers.
rm ./_release/agave-install ./_release/agave-install-init ./_release/solana-ledger-udev
# Excluded. 
# TODO: Why? Official binary release does not contain these, only libagave_*_program.so installed.
rm \
        ./_release/libsolana_frozen_abi_macro.so \
        ./_release/libsolana_package_metadata_macro.so \
        ./_release/libsolana_sdk_macro.so \
        ./_release/libsolana_sdk.so \
        ./_release/libsolana_zk_sdk.so \
        ./_release/libsolana_zk_token_sdk.so
rm ./_release/gen-syscall-list
rm ./_release/gen-headers
rm ./_release/proto
rm ./_release/agave-cargo-registry

mv ./_release/*.so \
        %{buildroot}/opt/agave/%{agave_suffix}/bin/deps/
mv ./_release/* \
        %{buildroot}/opt/agave/%{agave_suffix}/bin/

mv solana.bash-completion %{buildroot}/opt/agave/%{agave_suffix}/bin/solana.bash-completion


%files common
%dir /opt/agave
%dir /opt/agave/%{agave_suffix}
%dir /opt/agave/%{agave_suffix}/bin
%dir /opt/agave/%{agave_suffix}/bin/deps
%dir /opt/agave/%{agave_suffix}/bin/perf-libs
/opt/agave/%{agave_suffix}/activate


%files cli
%dir /opt/agave
%dir /opt/agave/%{agave_suffix}
%dir /opt/agave/%{agave_suffix}/bin
/opt/agave/%{agave_suffix}/bin/solana
/opt/agave/%{agave_suffix}/bin/solana-stake-accounts
/opt/agave/%{agave_suffix}/bin/solana-tokens
/opt/agave/%{agave_suffix}/bin/solana-keygen
/opt/agave/%{agave_suffix}/bin/solana-zk-keygen
/opt/agave/%{agave_suffix}/bin/solana.bash-completion


%files utils
%dir /opt/agave
%dir /opt/agave/%{agave_suffix}
%dir /opt/agave/%{agave_suffix}/bin
/opt/agave/%{agave_suffix}/bin/solana-upload-perf
/opt/agave/%{agave_suffix}/bin/solana-claim-mev-tips
/opt/agave/%{agave_suffix}/bin/solana-merkle-root-generator
/opt/agave/%{agave_suffix}/bin/solana-merkle-root-uploader
/opt/agave/%{agave_suffix}/bin/solana-gossip
/opt/agave/%{agave_suffix}/bin/solana-ip-address
/opt/agave/%{agave_suffix}/bin/solana-log-analyzer
/opt/agave/%{agave_suffix}/bin/solana-genesis


%files deps
%dir /opt/agave
%dir /opt/agave/%{agave_suffix}
%dir /opt/agave/%{agave_suffix}/bin
%dir /opt/agave/%{agave_suffix}/bin/deps
/opt/agave/%{agave_suffix}/bin/deps/libsolana_program.so


%files daemons
%dir /opt/agave
%dir /opt/agave/%{agave_suffix}
%dir /opt/agave/%{agave_suffix}/bin
/opt/agave/%{agave_suffix}/bin/solana-faucet
/opt/agave/%{agave_suffix}/bin/solana-ip-address-server
/opt/agave/%{agave_suffix}/bin/agave-validator
/opt/agave/%{agave_suffix}/bin/agave-watchtower
/opt/agave/%{agave_suffix}/bin/agave-accounts-hash-cache-tool
/opt/agave/%{agave_suffix}/bin/agave-ledger-tool
/opt/agave/%{agave_suffix}/bin/agave-store-tool
/opt/agave/%{agave_suffix}/bin/solana-net-shaper
/opt/agave/%{agave_suffix}/bin/solana-stake-meta-generator

%{_unitdir}/agave-validator-%{agave_suffix}.service
%{_unitdir}/agave-watchtower-%{agave_suffix}.service
%attr(0640,root,%{agave_group}) %config(noreplace) %{_sysconfdir}/sysconfig/agave-validator-%{agave_suffix}
%attr(0640,root,%{agave_group}) %config(noreplace) %{_sysconfdir}/sysconfig/agave-watchtower-%{agave_suffix}
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/logrotate.d/agave-validator-%{agave_suffix}

%attr(0755,root,root) %dir %{_sysconfdir}/agave
%attr(0750,root,%{agave_group}) %dir %{agave_etc}

%attr(0755,root,root) %dir %{_sharedstatedir}/agave
%attr(0750,%{agave_user},%{agave_group}) %dir %{agave_home}

%attr(0755,root,root) %dir %{_localstatedir}/log/agave
%attr(0750,%{agave_user},%{agave_group}) %dir %{agave_log}


%files bpf-utils
%dir /opt/agave
%dir /opt/agave/%{agave_suffix}
%dir /opt/agave/%{agave_suffix}/bin
/opt/agave/%{agave_suffix}/bin/cargo-build-bpf
/opt/agave/%{agave_suffix}/bin/cargo-test-bpf
/opt/agave/%{agave_suffix}/bin/rbpf-cli


%files sbf-utils
%dir /opt/agave
%dir /opt/agave/%{agave_suffix}
%dir /opt/agave/%{agave_suffix}/bin
/opt/agave/%{agave_suffix}/bin/cargo-build-sbf
/opt/agave/%{agave_suffix}/bin/cargo-test-sbf


%files tests
%dir /opt/agave
%dir /opt/agave/%{agave_suffix}
%dir /opt/agave/%{agave_suffix}/bin
/opt/agave/%{agave_suffix}/bin/solana-accounts-bench
/opt/agave/%{agave_suffix}/bin/solana-accounts-cluster-bench
/opt/agave/%{agave_suffix}/bin/solana-banking-bench
/opt/agave/%{agave_suffix}/bin/solana-bench-streamer
/opt/agave/%{agave_suffix}/bin/solana-bench-tps
/opt/agave/%{agave_suffix}/bin/solana-dos
/opt/agave/%{agave_suffix}/bin/solana-merkle-root-bench
/opt/agave/%{agave_suffix}/bin/solana-poh-bench
/opt/agave/%{agave_suffix}/bin/solana-test-validator
/opt/agave/%{agave_suffix}/bin/solana-transaction-dos


%pre daemons
# TODO: Separate user for each daemon.
getent group %{agave_group} >/dev/null || groupadd -r %{agave_group}
getent passwd %{agave_user} >/dev/null || \
        useradd -r -s /sbin/nologin -d %{agave_home} -M \
        -c 'Solana/Agave (%{agave_suffix})' -g %{agave_group} %{agave_user}
exit 0


%post daemons
%systemd_post agave-validator-%{agave_suffix}.service
%systemd_post agave-watchtower-%{agave_suffix}.service


%preun daemons
%systemd_preun agave-validator-%{agave_suffix}.service
%systemd_preun agave-watchtower-%{agave_suffix}.service


%postun daemons
%systemd_postun agave-validator-%{agave_suffix}.service
%systemd_postun_with_restart agave-watchtower-%{agave_suffix}.service


%changelog
* Sat Aug 31 2024 Ivan Mironov <mironov.ivan@gmail.com> - 2.0.8-1jito
- Update to 2.0.8

* Sat Aug 24 2024 Ivan Mironov <mironov.ivan@gmail.com> - 2.0.7-1jito
- Update to 2.0.7

* Fri Aug 09 2024 Ivan Mironov <mironov.ivan@gmail.com> - 2.0.5-1jito
- Update to 2.0.5

* Tue Aug 06 2024 Ivan Mironov <mironov.ivan@gmail.com> - 2.0.4-1jito
- Update to 2.0.4

* Mon Aug 5 2024 Ivan Mironov <mironov.ivan@gmail.com> - 2.0.3-1
- Initial packaging
