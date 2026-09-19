# -*- coding: utf-8-unix -*-

clean:
	rm -rf build
	rm -rf .flatpak-builder

install:
	$(MAKE) uninstall
	rm -rf build .flatpak-builder/build
	flatpak --user remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo
	flatpak-builder --install --install-deps-from=flathub build io.otsaloma.nfoview.yml

run:
	flatpak run io.otsaloma.nfoview

uninstall:
	flatpak uninstall -y io.otsaloma.nfoview/x86_64/master || true

.PHONY: clean install run uninstall
