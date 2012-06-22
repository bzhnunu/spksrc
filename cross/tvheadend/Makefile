PKG_NAME = tvheadend
PKG_VERS = 2.99-44-g4ef72fb
PKG_EXT = tar.gz
PKG_DIST_NAME = $(PKG_NAME)-$(PKG_VERS).$(PKG_EXT)
PKG_DIST_SITE = https://github.com/andoma/tvheadend/tarball/master
PKG_DIR = $(PKG_NAME)-$(PKG_VERS)

DEPENDS = cross/openssl

HOMEPAGE = https://www.lonelycoder.com/tvheadend/
COMMENT  = Tvheadend is a TV streaming server for Linux.
LICENSE  =

GNU_CONFIGURE = 1
CONFIGURE_ARGS = --disable-avahi

include ../../mk/spksrc.cross-cc.mk

