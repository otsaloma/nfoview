# -*- coding: utf-8-unix -*-

clean:
	rm -rf .flatpak-builder
	rm -rf build

install:
	$(MAKE) clean uninstall
	flatpak-builder --install --install-deps-from=flathub build io.otsaloma.nfoview.yml

run:
	flatpak run io.otsaloma.nfoview

uninstall:
	flatpak uninstall -y io.otsaloma.nfoview/x86_64/master || true

.PHONY: clean install run uninstall
