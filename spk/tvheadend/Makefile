SPK_NAME = tvheadend
SPK_VERS = 2.99-44-g4ef72fb
SPK_REV = 3
SPK_ICON = src/tvheadendlogo.png
DSM_UI_DIR = app

DEPENDS = cross/openssl cross/$(SPK_NAME)

MAINTAINER = SynoCommunity
DESCRIPTION = Tvheadend is a TV streaming server for Linux supporting DVB-S, DVB-S2, DVB-C, DVB-T, ATSC, IPTV, and Analog video \(V4L\) as input sources. It also comes with a powerful and easy to use web interface both used for configuration and day-to-day operations, such as searching the EPG and scheduling recordings. Even so, the most notable feature of Tvheadend is how easy it is to set up: Install it, navigate to the web user interface, drill into the TV adapters tab, select your current location and Tvheadend will start scanning channels and present them to you in just a few minutes.
ADMIN_PORT = 9981
RELOAD_UI = yes
DISPLAY_NAME = Tvheadend

HOMEPAGE = https://www.lonelycoder.com/tvheadend/
LICENSE  =

INSTALLER_SCRIPT = src/installer.sh
SSS_SCRIPT       = src/dsm-control.sh

INSTALL_PREFIX = /usr/local/$(SPK_NAME)

POST_STRIP_TARGET = tvheadend_extra_install

include ../../mk/spksrc.spk.mk

.PHONY: tvheadend_extra_install
tvheadend_extra_install:
	install -m 755 -d $(STAGING_DIR)/var
	install -m 755 -d $(STAGING_DIR)/app
	install -m 755 src/app/tvheadend.cgi.pl $(STAGING_DIR)/app/tvheadend.cgi
	install -m 755 -d $(STAGING_DIR)/app/images
	for size in 16 24 32 48 ; \
	do \
	    convert $(SPK_ICON) -thumbnail $${size}x$${size} \
	            $(STAGING_DIR)/app/images/$(SPK_NAME)-$${size}.png ; \
	done

