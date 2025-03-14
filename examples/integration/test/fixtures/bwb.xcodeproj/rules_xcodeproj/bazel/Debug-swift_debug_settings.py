#!/usr/bin/python3

"""An lldb module that registers a stop hook to set swift settings."""

import lldb
import re

# Order matters, it needs to be from the most nested to the least
_BUNDLE_EXTENSIONS = [
    ".framework",
    ".xctest",
    ".appex",
    ".bundle",
    ".app",
]

_TRIPLE_MATCH = re.compile(r"([^-]+-[^-]+)(-\D+)[^-]*(-.*)?")

_SETTINGS = {
	"arm64-apple-ios AppClip.app/AppClip": {
		"c": "-F$(PROJECT_DIR)/external/com_github_krzyzanowskim_cryptoswift/CryptoSwift.xcframework/ios-arm64_armv7 -iquote$(PROJECT_DIR)/external/com_github_krzyzanowskim_cryptoswift -iquote$(PROJECT_DIR)/bazel-out/ios-arm64-min15.0-applebin_ios-ios_arm64-dbg-STABLE-4/bin/external/com_github_krzyzanowskim_cryptoswift -iquote$(PROJECT_DIR) -iquote$(PROJECT_DIR)/bazel-out/ios-arm64-min15.0-applebin_ios-ios_arm64-dbg-STABLE-4/bin -fmodule-map-file=$(PROJECT_DIR)/external/com_github_krzyzanowskim_cryptoswift/CryptoSwift.xcframework/ios-arm64_armv7/CryptoSwift.framework/Modules/module.modulemap -O0 -DDEBUG=1 -fstack-protector -fstack-protector-all -iquote$(PROJECT_DIR)/external/com_github_krzyzanowskim_cryptoswift -iquote$(PROJECT_DIR)/bazel-out/ios-arm64-min15.0-applebin_ios-ios_arm64-dbg-STABLE-4/bin/external/com_github_krzyzanowskim_cryptoswift -iquote$(PROJECT_DIR) -iquote$(PROJECT_DIR)/bazel-out/ios-arm64-min15.0-applebin_ios-ios_arm64-dbg-STABLE-4/bin -O0 -fstack-protector -fstack-protector-all",
		"f": [
			"$(BAZEL_EXTERNAL)/com_github_krzyzanowskim_cryptoswift/CryptoSwift.xcframework/ios-arm64_armv7"
		],
		"s": [
			"$(BAZEL_OUT)/ios-arm64-min15.0-applebin_ios-ios_arm64-dbg-STABLE-4/bin/Lib"
		]
	},
	"arm64-apple-ios Lib.framework/Lib": {
		"c": "-F$(PROJECT_DIR)/external/com_github_krzyzanowskim_cryptoswift/CryptoSwift.xcframework/ios-arm64_armv7 -iquote$(PROJECT_DIR)/external/com_github_krzyzanowskim_cryptoswift -iquote$(PROJECT_DIR)/bazel-out/ios-arm64-min15.0-applebin_ios-ios_arm64-dbg-STABLE-4/bin/external/com_github_krzyzanowskim_cryptoswift -iquote$(PROJECT_DIR) -iquote$(PROJECT_DIR)/bazel-out/ios-arm64-min15.0-applebin_ios-ios_arm64-dbg-STABLE-4/bin -fmodule-map-file=$(PROJECT_DIR)/external/com_github_krzyzanowskim_cryptoswift/CryptoSwift.xcframework/ios-arm64_armv7/CryptoSwift.framework/Modules/module.modulemap -O0 -DDEBUG=1 -fstack-protector -fstack-protector-all",
		"f": [
			"$(BAZEL_EXTERNAL)/com_github_krzyzanowskim_cryptoswift/CryptoSwift.xcframework/ios-arm64_armv7"
		]
	},
	"arm64-apple-ios UIFramework.iOS.framework/UIFramework.iOS": {
		"c": "-F$(PROJECT_DIR)/external/com_github_krzyzanowskim_cryptoswift/CryptoSwift.xcframework/ios-arm64_armv7 -iquote$(PROJECT_DIR)/external/com_github_krzyzanowskim_cryptoswift -iquote$(PROJECT_DIR)/bazel-out/ios-arm64-min15.0-applebin_ios-ios_arm64-dbg-STABLE-4/bin/external/com_github_krzyzanowskim_cryptoswift -iquote$(PROJECT_DIR) -iquote$(PROJECT_DIR)/bazel-out/ios-arm64-min15.0-applebin_ios-ios_arm64-dbg-STABLE-4/bin -fmodule-map-file=$(PROJECT_DIR)/external/com_github_krzyzanowskim_cryptoswift/CryptoSwift.xcframework/ios-arm64_armv7/CryptoSwift.framework/Modules/module.modulemap -O0 -DDEBUG=1 -fstack-protector -fstack-protector-all -iquote$(PROJECT_DIR)/external/com_github_krzyzanowskim_cryptoswift -iquote$(PROJECT_DIR)/bazel-out/ios-arm64-min15.0-applebin_ios-ios_arm64-dbg-STABLE-4/bin/external/com_github_krzyzanowskim_cryptoswift -iquote$(PROJECT_DIR) -iquote$(PROJECT_DIR)/bazel-out/ios-arm64-min15.0-applebin_ios-ios_arm64-dbg-STABLE-4/bin -O0 -fstack-protector -fstack-protector-all",
		"f": [
			"$(BAZEL_EXTERNAL)/com_github_krzyzanowskim_cryptoswift/CryptoSwift.xcframework/ios-arm64_armv7"
		],
		"s": [
			"$(BAZEL_OUT)/ios-arm64-min15.0-applebin_ios-ios_arm64-dbg-STABLE-4/bin/Lib"
		]
	},
	"arm64-apple-ios WidgetExtension.appex/WidgetExtension": {
		"c": "-F$(PROJECT_DIR)/external/com_github_krzyzanowskim_cryptoswift/CryptoSwift.xcframework/ios-arm64_armv7 -iquote$(PROJECT_DIR)/external/com_github_krzyzanowskim_cryptoswift -iquote$(PROJECT_DIR)/bazel-out/ios-arm64-min15.0-applebin_ios-ios_arm64-dbg-STABLE-4/bin/external/com_github_krzyzanowskim_cryptoswift -iquote$(PROJECT_DIR) -iquote$(PROJECT_DIR)/bazel-out/ios-arm64-min15.0-applebin_ios-ios_arm64-dbg-STABLE-4/bin -fmodule-map-file=$(PROJECT_DIR)/external/com_github_krzyzanowskim_cryptoswift/CryptoSwift.xcframework/ios-arm64_armv7/CryptoSwift.framework/Modules/module.modulemap -O0 -DDEBUG=1 -fstack-protector -fstack-protector-all -iquote$(PROJECT_DIR)/external/com_github_krzyzanowskim_cryptoswift -iquote$(PROJECT_DIR)/bazel-out/ios-arm64-min15.0-applebin_ios-ios_arm64-dbg-STABLE-4/bin/external/com_github_krzyzanowskim_cryptoswift -iquote$(PROJECT_DIR) -iquote$(PROJECT_DIR)/bazel-out/ios-arm64-min15.0-applebin_ios-ios_arm64-dbg-STABLE-4/bin -O0 -fstack-protector -fstack-protector-all",
		"f": [
			"$(BAZEL_EXTERNAL)/com_github_krzyzanowskim_cryptoswift/CryptoSwift.xcframework/ios-arm64_armv7"
		],
		"s": [
			"$(BAZEL_OUT)/ios-arm64-min15.0-applebin_ios-ios_arm64-dbg-STABLE-4/bin/Lib"
		]
	},
	"arm64-apple-ios iOSApp.app/iOSApp_ExecutableName": {
		"c": "-F$(PROJECT_DIR)/external/com_github_krzyzanowskim_cryptoswift/CryptoSwift.xcframework/ios-arm64_armv7 -F$(PROJECT_DIR)/external/com_google_google_maps/GoogleMaps.xcframework/ios-arm64 -F$(PROJECT_DIR)/external/com_google_google_maps/GoogleMapsCore.xcframework/ios-arm64 -F$(PROJECT_DIR)/external/com_google_google_maps/GoogleMapsBase.xcframework/ios-arm64 -I$(PROJECT_DIR)/iOSApp/Source/CoreUtilsObjC -I$(PROJECT_DIR)/bazel-out/ios-arm64-min15.0-applebin_ios-ios_arm64-dbg-STABLE-4/bin/iOSApp/Source/CoreUtilsObjC -iquote$(PROJECT_DIR)/external/com_github_krzyzanowskim_cryptoswift -iquote$(PROJECT_DIR)/bazel-out/ios-arm64-min15.0-applebin_ios-ios_arm64-dbg-STABLE-4/bin/external/com_github_krzyzanowskim_cryptoswift -iquote$(PROJECT_DIR) -iquote$(PROJECT_DIR)/bazel-out/ios-arm64-min15.0-applebin_ios-ios_arm64-dbg-STABLE-4/bin -iquote$(PROJECT_DIR)/external/com_google_google_maps -iquote$(PROJECT_DIR)/bazel-out/ios-arm64-min15.0-applebin_ios-ios_arm64-dbg-STABLE-4/bin/external/com_google_google_maps -DNEEDS_QUOTES=Two\\ words -fmodule-map-file=$(PROJECT_DIR)/external/com_github_krzyzanowskim_cryptoswift/CryptoSwift.xcframework/ios-arm64_armv7/CryptoSwift.framework/Modules/module.modulemap -fmodule-map-file=$(PROJECT_DIR)/bazel-out/ios-arm64-min15.0-applebin_ios-ios_arm64-dbg-STABLE-4/bin/iOSApp/Source/CoreUtilsMixed/MixedAnswer/MixedAnswer_objc_modulemap.swift.modulemap -fmodule-map-file=$(PROJECT_DIR)/bazel-out/ios-arm64-min15.0-applebin_ios-ios_arm64-dbg-STABLE-4/bin/iOSApp/Source/CoreUtilsMixed/MixedAnswer/MixedAnswer_swift_modulemap.swift.modulemap -fmodule-map-file=$(PROJECT_DIR)/bazel-out/ios-arm64-min15.0-applebin_ios-ios_arm64-dbg-STABLE-4/bin/iOSApp/Source/CoreUtilsMixed/MixedAnswer/MixedAnswer_objc_modulemap-module.modulemap -fmodule-map-file=$(PROJECT_DIR)/bazel-out/ios-arm64-min15.0-applebin_ios-ios_arm64-dbg-STABLE-4/bin/iOSApp/Source/CoreUtilsObjC/CoreUtilsObjC.swift.modulemap -fmodule-map-file=$(PROJECT_DIR)/external/com_google_google_maps/GoogleMapsBase.xcframework/ios-arm64/GoogleMapsBase.framework/Modules/module.modulemap -fmodule-map-file=$(PROJECT_DIR)/external/com_google_google_maps/GoogleMapsCore.xcframework/ios-arm64/GoogleMapsCore.framework/Modules/module.modulemap -fmodule-map-file=$(PROJECT_DIR)/external/com_google_google_maps/GoogleMaps.xcframework/ios-arm64/GoogleMaps.framework/Modules/module.modulemap -O0 -DDEBUG=1 -fstack-protector -fstack-protector-all -iquote$(PROJECT_DIR)/external/com_github_krzyzanowskim_cryptoswift -iquote$(PROJECT_DIR)/bazel-out/ios-arm64-min15.0-applebin_ios-ios_arm64-dbg-STABLE-4/bin/external/com_github_krzyzanowskim_cryptoswift -iquote$(PROJECT_DIR) -iquote$(PROJECT_DIR)/bazel-out/ios-arm64-min15.0-applebin_ios-ios_arm64-dbg-STABLE-4/bin -O0 -fstack-protector -fstack-protector-all -iquote$(PROJECT_DIR)/external/com_github_krzyzanowskim_cryptoswift -iquote$(PROJECT_DIR)/bazel-out/ios-arm64-min15.0-applebin_ios-ios_arm64-dbg-STABLE-4/bin/external/com_github_krzyzanowskim_cryptoswift -iquote$(PROJECT_DIR) -iquote$(PROJECT_DIR)/bazel-out/ios-arm64-min15.0-applebin_ios-ios_arm64-dbg-STABLE-4/bin -O0 -fstack-protector -fstack-protector-all -iquote$(PROJECT_DIR) -iquote$(PROJECT_DIR)/bazel-out/ios-arm64-min15.0-applebin_ios-ios_arm64-dbg-STABLE-4/bin -O0 -fstack-protector -fstack-protector-all",
		"f": [
			"$(BAZEL_EXTERNAL)/com_google_google_maps/GoogleMapsBase.xcframework/ios-arm64",
			"$(BAZEL_EXTERNAL)/com_google_google_maps/GoogleMapsCore.xcframework/ios-arm64",
			"$(BAZEL_EXTERNAL)/com_google_google_maps/GoogleMaps.xcframework/ios-arm64",
			"$(BAZEL_EXTERNAL)/com_github_krzyzanowskim_cryptoswift/CryptoSwift.xcframework/ios-arm64_armv7"
		],
		"s": [
			"$(BAZEL_OUT)/ios-arm64-min15.0-applebin_ios-ios_arm64-dbg-STABLE-4/bin/UI",
			"$(BAZEL_OUT)/ios-arm64-min15.0-applebin_ios-ios_arm64-dbg-STABLE-4/bin/iOSApp/Source/CoreUtilsMixed/MixedAnswer",
			"$(BAZEL_OUT)/ios-arm64-min15.0-applebin_ios-ios_arm64-dbg-STABLE-4/bin/Lib"
		]
	},
	"arm64-apple-macosx tool.binary": {
		"c": "-F$(PROJECT_DIR)/external/examples_command_line_external -I$(SDKROOT)/usr/include/uuid -iquote$(PROJECT_DIR) -iquote$(PROJECT_DIR)/bazel-out/macos-arm64-min11.0-applebin_macos-darwin_arm64-dbg-STABLE-34/bin -iquote$(PROJECT_DIR)/external/examples_command_line_external -iquote$(PROJECT_DIR)/bazel-out/macos-arm64-min11.0-applebin_macos-darwin_arm64-dbg-STABLE-34/bin/external/examples_command_line_external -DSECRET_3=\"Hello\" -DSECRET_2=\"World!\" -fmodule-map-file=$(PROJECT_DIR)/bazel-out/macos-arm64-min11.0-applebin_macos-darwin_arm64-dbg-STABLE-34/bin/CommandLine/CommandLineToolLib/lib_impl.swift.modulemap -fmodule-map-file=$(PROJECT_DIR)/CommandLine/swift_c_module/c_lib.modulemap -fmodule-map-file=$(PROJECT_DIR)/external/examples_command_line_external/ExternalFramework.framework/Modules/module.modulemap -fmodule-map-file=$(PROJECT_DIR)/bazel-out/macos-arm64-min11.0-applebin_macos-darwin_arm64-dbg-STABLE-34/bin/external/examples_command_line_external/Library.swift.modulemap -fmodule-map-file=$(PROJECT_DIR)/bazel-out/macos-arm64-min11.0-applebin_macos-darwin_arm64-dbg-STABLE-34/bin/CommandLine/CommandLineToolLib/private_lib.swift.modulemap -O0 -DDEBUG=1 -fstack-protector -fstack-protector-all -iquote$(PROJECT_DIR) -iquote$(PROJECT_DIR)/bazel-out/macos-arm64-min11.0-applebin_macos-darwin_arm64-dbg-STABLE-34/bin -O0 -fstack-protector -fstack-protector-all",
		"f": [
			"$(BAZEL_EXTERNAL)/examples_command_line_external"
		],
		"s": [
			"$(BAZEL_OUT)/macos-arm64-min11.0-applebin_macos-darwin_arm64-dbg-STABLE-34/bin/CommandLine/CommandLineToolLib"
		]
	},
	"arm64-apple-tvos Lib.framework/Lib": {
		"c": "-F$(PROJECT_DIR)/external/com_github_krzyzanowskim_cryptoswift/CryptoSwift.xcframework/tvos-arm64 -iquote$(PROJECT_DIR)/external/com_github_krzyzanowskim_cryptoswift -iquote$(PROJECT_DIR)/bazel-out/tvos-arm64-min15.0-applebin_tvos-tvos_arm64-dbg-STABLE-6/bin/external/com_github_krzyzanowskim_cryptoswift -iquote$(PROJECT_DIR) -iquote$(PROJECT_DIR)/bazel-out/tvos-arm64-min15.0-applebin_tvos-tvos_arm64-dbg-STABLE-6/bin -fmodule-map-file=$(PROJECT_DIR)/external/com_github_krzyzanowskim_cryptoswift/CryptoSwift.xcframework/tvos-arm64/CryptoSwift.framework/Modules/module.modulemap -O0 -DDEBUG=1 -fstack-protector -fstack-protector-all",
		"f": [
			"$(BAZEL_EXTERNAL)/com_github_krzyzanowskim_cryptoswift/CryptoSwift.xcframework/tvos-arm64"
		]
	},
	"arm64-apple-tvos LibFramework.tvOS.framework/LibFramework.tvOS": {
		"c": "-F$(PROJECT_DIR)/external/com_github_krzyzanowskim_cryptoswift/CryptoSwift.xcframework/tvos-arm64 -iquote$(PROJECT_DIR)/external/com_github_krzyzanowskim_cryptoswift -iquote$(PROJECT_DIR)/bazel-out/tvos-arm64-min15.0-applebin_tvos-tvos_arm64-dbg-STABLE-6/bin/external/com_github_krzyzanowskim_cryptoswift -iquote$(PROJECT_DIR) -iquote$(PROJECT_DIR)/bazel-out/tvos-arm64-min15.0-applebin_tvos-tvos_arm64-dbg-STABLE-6/bin -fmodule-map-file=$(PROJECT_DIR)/external/com_github_krzyzanowskim_cryptoswift/CryptoSwift.xcframework/tvos-arm64/CryptoSwift.framework/Modules/module.modulemap -O0 -DDEBUG=1 -fstack-protector -fstack-protector-all",
		"f": [
			"$(BAZEL_EXTERNAL)/com_github_krzyzanowskim_cryptoswift/CryptoSwift.xcframework/tvos-arm64"
		]
	},
	"arm64-apple-tvos UIFramework.tvOS.framework/UIFramework.tvOS": {
		"c": "-F$(PROJECT_DIR)/external/com_github_krzyzanowskim_cryptoswift/CryptoSwift.xcframework/tvos-arm64 -iquote$(PROJECT_DIR)/external/com_github_krzyzanowskim_cryptoswift -iquote$(PROJECT_DIR)/bazel-out/tvos-arm64-min15.0-applebin_tvos-tvos_arm64-dbg-STABLE-6/bin/external/com_github_krzyzanowskim_cryptoswift -iquote$(PROJECT_DIR) -iquote$(PROJECT_DIR)/bazel-out/tvos-arm64-min15.0-applebin_tvos-tvos_arm64-dbg-STABLE-6/bin -fmodule-map-file=$(PROJECT_DIR)/external/com_github_krzyzanowskim_cryptoswift/CryptoSwift.xcframework/tvos-arm64/CryptoSwift.framework/Modules/module.modulemap -O0 -DDEBUG=1 -fstack-protector -fstack-protector-all -iquote$(PROJECT_DIR)/external/com_github_krzyzanowskim_cryptoswift -iquote$(PROJECT_DIR)/bazel-out/tvos-arm64-min15.0-applebin_tvos-tvos_arm64-dbg-STABLE-6/bin/external/com_github_krzyzanowskim_cryptoswift -iquote$(PROJECT_DIR) -iquote$(PROJECT_DIR)/bazel-out/tvos-arm64-min15.0-applebin_tvos-tvos_arm64-dbg-STABLE-6/bin -O0 -fstack-protector -fstack-protector-all",
		"f": [
			"$(BAZEL_EXTERNAL)/com_github_krzyzanowskim_cryptoswift/CryptoSwift.xcframework/tvos-arm64"
		],
		"s": [
			"$(BAZEL_OUT)/tvos-arm64-min15.0-applebin_tvos-tvos_arm64-dbg-STABLE-6/bin/Lib"
		]
	},
	"arm64-apple-tvos tvOSApp.app/tvOSApp": {
		"c": "-F$(PROJECT_DIR)/external/com_github_krzyzanowskim_cryptoswift/CryptoSwift.xcframework/tvos-arm64 -iquote$(PROJECT_DIR)/external/com_github_krzyzanowskim_cryptoswift -iquote$(PROJECT_DIR)/bazel-out/tvos-arm64-min15.0-applebin_tvos-tvos_arm64-dbg-STABLE-6/bin/external/com_github_krzyzanowskim_cryptoswift -iquote$(PROJECT_DIR) -iquote$(PROJECT_DIR)/bazel-out/tvos-arm64-min15.0-applebin_tvos-tvos_arm64-dbg-STABLE-6/bin -fmodule-map-file=$(PROJECT_DIR)/external/com_github_krzyzanowskim_cryptoswift/CryptoSwift.xcframework/tvos-arm64/CryptoSwift.framework/Modules/module.modulemap -O0 -DDEBUG=1 -fstack-protector -fstack-protector-all -iquote$(PROJECT_DIR)/external/com_github_krzyzanowskim_cryptoswift -iquote$(PROJECT_DIR)/bazel-out/tvos-arm64-min15.0-applebin_tvos-tvos_arm64-dbg-STABLE-6/bin/external/com_github_krzyzanowskim_cryptoswift -iquote$(PROJECT_DIR) -iquote$(PROJECT_DIR)/bazel-out/tvos-arm64-min15.0-applebin_tvos-tvos_arm64-dbg-STABLE-6/bin -O0 -fstack-protector -fstack-protector-all -iquote$(PROJECT_DIR)/external/com_github_krzyzanowskim_cryptoswift -iquote$(PROJECT_DIR)/bazel-out/tvos-arm64-min15.0-applebin_tvos-tvos_arm64-dbg-STABLE-6/bin/external/com_github_krzyzanowskim_cryptoswift -iquote$(PROJECT_DIR) -iquote$(PROJECT_DIR)/bazel-out/tvos-arm64-min15.0-applebin_tvos-tvos_arm64-dbg-STABLE-6/bin -O0 -fstack-protector -fstack-protector-all",
		"f": [
			"$(BAZEL_EXTERNAL)/com_github_krzyzanowskim_cryptoswift/CryptoSwift.xcframework/tvos-arm64"
		],
		"s": [
			"$(BAZEL_OUT)/tvos-arm64-min15.0-applebin_tvos-tvos_arm64-dbg-STABLE-6/bin/UI",
			"$(BAZEL_OUT)/tvos-arm64-min15.0-applebin_tvos-tvos_arm64-dbg-STABLE-6/bin/Lib"
		]
	},
	"arm64_32-apple-watchos Lib.framework/Lib": {
		"c": "-F$(PROJECT_DIR)/external/com_github_krzyzanowskim_cryptoswift/CryptoSwift.xcframework/watchos-arm64_32_armv7k -iquote$(PROJECT_DIR)/external/com_github_krzyzanowskim_cryptoswift -iquote$(PROJECT_DIR)/bazel-out/watchos-arm64_32-min7.0-applebin_watchos-watchos_arm64_32-dbg-STABLE-5/bin/external/com_github_krzyzanowskim_cryptoswift -iquote$(PROJECT_DIR) -iquote$(PROJECT_DIR)/bazel-out/watchos-arm64_32-min7.0-applebin_watchos-watchos_arm64_32-dbg-STABLE-5/bin -fmodule-map-file=$(PROJECT_DIR)/external/com_github_krzyzanowskim_cryptoswift/CryptoSwift.xcframework/watchos-arm64_32_armv7k/CryptoSwift.framework/Modules/module.modulemap -O0 -DDEBUG=1 -fstack-protector -fstack-protector-all",
		"f": [
			"$(BAZEL_EXTERNAL)/com_github_krzyzanowskim_cryptoswift/CryptoSwift.xcframework/watchos-arm64_32_armv7k"
		]
	},
	"arm64_32-apple-watchos LibFramework.watchOS.framework/LibFramework.watchOS": {
		"c": "-F$(PROJECT_DIR)/external/com_github_krzyzanowskim_cryptoswift/CryptoSwift.xcframework/watchos-arm64_32_armv7k -iquote$(PROJECT_DIR)/external/com_github_krzyzanowskim_cryptoswift -iquote$(PROJECT_DIR)/bazel-out/watchos-arm64_32-min7.0-applebin_watchos-watchos_arm64_32-dbg-STABLE-5/bin/external/com_github_krzyzanowskim_cryptoswift -iquote$(PROJECT_DIR) -iquote$(PROJECT_DIR)/bazel-out/watchos-arm64_32-min7.0-applebin_watchos-watchos_arm64_32-dbg-STABLE-5/bin -fmodule-map-file=$(PROJECT_DIR)/external/com_github_krzyzanowskim_cryptoswift/CryptoSwift.xcframework/watchos-arm64_32_armv7k/CryptoSwift.framework/Modules/module.modulemap -O0 -DDEBUG=1 -fstack-protector -fstack-protector-all",
		"f": [
			"$(BAZEL_EXTERNAL)/com_github_krzyzanowskim_cryptoswift/CryptoSwift.xcframework/watchos-arm64_32_armv7k"
		]
	},
	"arm64_32-apple-watchos UIFramework.watchOS.framework/UIFramework.watchOS": {
		"c": "-F$(PROJECT_DIR)/external/com_github_krzyzanowskim_cryptoswift/CryptoSwift.xcframework/watchos-arm64_32_armv7k -iquote$(PROJECT_DIR)/external/com_github_krzyzanowskim_cryptoswift -iquote$(PROJECT_DIR)/bazel-out/watchos-arm64_32-min7.0-applebin_watchos-watchos_arm64_32-dbg-STABLE-5/bin/external/com_github_krzyzanowskim_cryptoswift -iquote$(PROJECT_DIR) -iquote$(PROJECT_DIR)/bazel-out/watchos-arm64_32-min7.0-applebin_watchos-watchos_arm64_32-dbg-STABLE-5/bin -fmodule-map-file=$(PROJECT_DIR)/external/com_github_krzyzanowskim_cryptoswift/CryptoSwift.xcframework/watchos-arm64_32_armv7k/CryptoSwift.framework/Modules/module.modulemap -O0 -DDEBUG=1 -fstack-protector -fstack-protector-all -iquote$(PROJECT_DIR)/external/com_github_krzyzanowskim_cryptoswift -iquote$(PROJECT_DIR)/bazel-out/watchos-arm64_32-min7.0-applebin_watchos-watchos_arm64_32-dbg-STABLE-5/bin/external/com_github_krzyzanowskim_cryptoswift -iquote$(PROJECT_DIR) -iquote$(PROJECT_DIR)/bazel-out/watchos-arm64_32-min7.0-applebin_watchos-watchos_arm64_32-dbg-STABLE-5/bin -O0 -fstack-protector -fstack-protector-all",
		"f": [
			"$(BAZEL_EXTERNAL)/com_github_krzyzanowskim_cryptoswift/CryptoSwift.xcframework/watchos-arm64_32_armv7k"
		],
		"s": [
			"$(BAZEL_OUT)/watchos-arm64_32-min7.0-applebin_watchos-watchos_arm64_32-dbg-STABLE-5/bin/Lib"
		]
	},
	"arm64_32-apple-watchos watchOSAppExtension.appex/watchOSAppExtension": {
		"c": "-F$(PROJECT_DIR)/external/com_github_krzyzanowskim_cryptoswift/CryptoSwift.xcframework/watchos-arm64_32_armv7k -iquote$(PROJECT_DIR)/external/com_github_krzyzanowskim_cryptoswift -iquote$(PROJECT_DIR)/bazel-out/watchos-arm64_32-min7.0-applebin_watchos-watchos_arm64_32-dbg-STABLE-5/bin/external/com_github_krzyzanowskim_cryptoswift -iquote$(PROJECT_DIR) -iquote$(PROJECT_DIR)/bazel-out/watchos-arm64_32-min7.0-applebin_watchos-watchos_arm64_32-dbg-STABLE-5/bin -fmodule-map-file=$(PROJECT_DIR)/external/com_github_krzyzanowskim_cryptoswift/CryptoSwift.xcframework/watchos-arm64_32_armv7k/CryptoSwift.framework/Modules/module.modulemap -O0 -DDEBUG=1 -fstack-protector -fstack-protector-all -iquote$(PROJECT_DIR)/external/com_github_krzyzanowskim_cryptoswift -iquote$(PROJECT_DIR)/bazel-out/watchos-arm64_32-min7.0-applebin_watchos-watchos_arm64_32-dbg-STABLE-5/bin/external/com_github_krzyzanowskim_cryptoswift -iquote$(PROJECT_DIR) -iquote$(PROJECT_DIR)/bazel-out/watchos-arm64_32-min7.0-applebin_watchos-watchos_arm64_32-dbg-STABLE-5/bin -O0 -fstack-protector -fstack-protector-all -iquote$(PROJECT_DIR)/external/com_github_krzyzanowskim_cryptoswift -iquote$(PROJECT_DIR)/bazel-out/watchos-arm64_32-min7.0-applebin_watchos-watchos_arm64_32-dbg-STABLE-5/bin/external/com_github_krzyzanowskim_cryptoswift -iquote$(PROJECT_DIR) -iquote$(PROJECT_DIR)/bazel-out/watchos-arm64_32-min7.0-applebin_watchos-watchos_arm64_32-dbg-STABLE-5/bin -O0 -fstack-protector -fstack-protector-all",
		"f": [
			"$(BAZEL_EXTERNAL)/com_github_krzyzanowskim_cryptoswift/CryptoSwift.xcframework/watchos-arm64_32_armv7k"
		],
		"s": [
			"$(BAZEL_OUT)/watchos-arm64_32-min7.0-applebin_watchos-watchos_arm64_32-dbg-STABLE-5/bin/UI",
			"$(BAZEL_OUT)/watchos-arm64_32-min7.0-applebin_watchos-watchos_arm64_32-dbg-STABLE-5/bin/Lib"
		]
	},
	"x86_64-apple-ios-simulator AppClip.app/AppClip": {
		"c": "-F$(PROJECT_DIR)/external/com_github_krzyzanowskim_cryptoswift/CryptoSwift.xcframework/ios-arm64_i386_x86_64-simulator -iquote$(PROJECT_DIR)/external/com_github_krzyzanowskim_cryptoswift -iquote$(PROJECT_DIR)/bazel-out/ios-x86_64-min15.0-applebin_ios-ios_x86_64-dbg-STABLE-1/bin/external/com_github_krzyzanowskim_cryptoswift -iquote$(PROJECT_DIR) -iquote$(PROJECT_DIR)/bazel-out/ios-x86_64-min15.0-applebin_ios-ios_x86_64-dbg-STABLE-1/bin -fmodule-map-file=$(PROJECT_DIR)/external/com_github_krzyzanowskim_cryptoswift/CryptoSwift.xcframework/ios-arm64_i386_x86_64-simulator/CryptoSwift.framework/Modules/module.modulemap -O0 -DDEBUG=1 -fstack-protector -fstack-protector-all -iquote$(PROJECT_DIR)/external/com_github_krzyzanowskim_cryptoswift -iquote$(PROJECT_DIR)/bazel-out/ios-x86_64-min15.0-applebin_ios-ios_x86_64-dbg-STABLE-1/bin/external/com_github_krzyzanowskim_cryptoswift -iquote$(PROJECT_DIR) -iquote$(PROJECT_DIR)/bazel-out/ios-x86_64-min15.0-applebin_ios-ios_x86_64-dbg-STABLE-1/bin -O0 -fstack-protector -fstack-protector-all",
		"f": [
			"$(BAZEL_EXTERNAL)/com_github_krzyzanowskim_cryptoswift/CryptoSwift.xcframework/ios-arm64_i386_x86_64-simulator"
		],
		"s": [
			"$(BAZEL_OUT)/ios-x86_64-min15.0-applebin_ios-ios_x86_64-dbg-STABLE-1/bin/Lib"
		]
	},
	"x86_64-apple-ios-simulator Lib.framework/Lib": {
		"c": "-F$(PROJECT_DIR)/external/com_github_krzyzanowskim_cryptoswift/CryptoSwift.xcframework/ios-arm64_i386_x86_64-simulator -iquote$(PROJECT_DIR)/external/com_github_krzyzanowskim_cryptoswift -iquote$(PROJECT_DIR)/bazel-out/ios-x86_64-min15.0-applebin_ios-ios_x86_64-dbg-STABLE-1/bin/external/com_github_krzyzanowskim_cryptoswift -iquote$(PROJECT_DIR) -iquote$(PROJECT_DIR)/bazel-out/ios-x86_64-min15.0-applebin_ios-ios_x86_64-dbg-STABLE-1/bin -fmodule-map-file=$(PROJECT_DIR)/external/com_github_krzyzanowskim_cryptoswift/CryptoSwift.xcframework/ios-arm64_i386_x86_64-simulator/CryptoSwift.framework/Modules/module.modulemap -O0 -DDEBUG=1 -fstack-protector -fstack-protector-all",
		"f": [
			"$(BAZEL_EXTERNAL)/com_github_krzyzanowskim_cryptoswift/CryptoSwift.xcframework/ios-arm64_i386_x86_64-simulator"
		]
	},
	"x86_64-apple-ios-simulator UIFramework.iOS.framework/UIFramework.iOS": {
		"c": "-F$(PROJECT_DIR)/external/com_github_krzyzanowskim_cryptoswift/CryptoSwift.xcframework/ios-arm64_i386_x86_64-simulator -iquote$(PROJECT_DIR)/external/com_github_krzyzanowskim_cryptoswift -iquote$(PROJECT_DIR)/bazel-out/ios-x86_64-min15.0-applebin_ios-ios_x86_64-dbg-STABLE-1/bin/external/com_github_krzyzanowskim_cryptoswift -iquote$(PROJECT_DIR) -iquote$(PROJECT_DIR)/bazel-out/ios-x86_64-min15.0-applebin_ios-ios_x86_64-dbg-STABLE-1/bin -fmodule-map-file=$(PROJECT_DIR)/external/com_github_krzyzanowskim_cryptoswift/CryptoSwift.xcframework/ios-arm64_i386_x86_64-simulator/CryptoSwift.framework/Modules/module.modulemap -O0 -DDEBUG=1 -fstack-protector -fstack-protector-all -iquote$(PROJECT_DIR)/external/com_github_krzyzanowskim_cryptoswift -iquote$(PROJECT_DIR)/bazel-out/ios-x86_64-min15.0-applebin_ios-ios_x86_64-dbg-STABLE-1/bin/external/com_github_krzyzanowskim_cryptoswift -iquote$(PROJECT_DIR) -iquote$(PROJECT_DIR)/bazel-out/ios-x86_64-min15.0-applebin_ios-ios_x86_64-dbg-STABLE-1/bin -O0 -fstack-protector -fstack-protector-all",
		"f": [
			"$(BAZEL_EXTERNAL)/com_github_krzyzanowskim_cryptoswift/CryptoSwift.xcframework/ios-arm64_i386_x86_64-simulator"
		],
		"s": [
			"$(BAZEL_OUT)/ios-x86_64-min15.0-applebin_ios-ios_x86_64-dbg-STABLE-1/bin/Lib"
		]
	},
	"x86_64-apple-ios-simulator WidgetExtension.appex/WidgetExtension": {
		"c": "-F$(PROJECT_DIR)/external/com_github_krzyzanowskim_cryptoswift/CryptoSwift.xcframework/ios-arm64_i386_x86_64-simulator -iquote$(PROJECT_DIR)/external/com_github_krzyzanowskim_cryptoswift -iquote$(PROJECT_DIR)/bazel-out/ios-x86_64-min15.0-applebin_ios-ios_x86_64-dbg-STABLE-1/bin/external/com_github_krzyzanowskim_cryptoswift -iquote$(PROJECT_DIR) -iquote$(PROJECT_DIR)/bazel-out/ios-x86_64-min15.0-applebin_ios-ios_x86_64-dbg-STABLE-1/bin -fmodule-map-file=$(PROJECT_DIR)/external/com_github_krzyzanowskim_cryptoswift/CryptoSwift.xcframework/ios-arm64_i386_x86_64-simulator/CryptoSwift.framework/Modules/module.modulemap -O0 -DDEBUG=1 -fstack-protector -fstack-protector-all -iquote$(PROJECT_DIR)/external/com_github_krzyzanowskim_cryptoswift -iquote$(PROJECT_DIR)/bazel-out/ios-x86_64-min15.0-applebin_ios-ios_x86_64-dbg-STABLE-1/bin/external/com_github_krzyzanowskim_cryptoswift -iquote$(PROJECT_DIR) -iquote$(PROJECT_DIR)/bazel-out/ios-x86_64-min15.0-applebin_ios-ios_x86_64-dbg-STABLE-1/bin -O0 -fstack-protector -fstack-protector-all",
		"f": [
			"$(BAZEL_EXTERNAL)/com_github_krzyzanowskim_cryptoswift/CryptoSwift.xcframework/ios-arm64_i386_x86_64-simulator"
		],
		"s": [
			"$(BAZEL_OUT)/ios-x86_64-min15.0-applebin_ios-ios_x86_64-dbg-STABLE-1/bin/Lib"
		]
	},
	"x86_64-apple-ios-simulator iMessageAppExtension.appex/iMessageAppExtension": {
		"c": "-F$(PROJECT_DIR)/external/com_github_krzyzanowskim_cryptoswift/CryptoSwift.xcframework/ios-arm64_i386_x86_64-simulator -iquote$(PROJECT_DIR)/external/com_github_krzyzanowskim_cryptoswift -iquote$(PROJECT_DIR)/bazel-out/ios-x86_64-min15.0-applebin_ios-ios_x86_64-dbg-STABLE-1/bin/external/com_github_krzyzanowskim_cryptoswift -iquote$(PROJECT_DIR) -iquote$(PROJECT_DIR)/bazel-out/ios-x86_64-min15.0-applebin_ios-ios_x86_64-dbg-STABLE-1/bin -fmodule-map-file=$(PROJECT_DIR)/external/com_github_krzyzanowskim_cryptoswift/CryptoSwift.xcframework/ios-arm64_i386_x86_64-simulator/CryptoSwift.framework/Modules/module.modulemap -O0 -DDEBUG=1 -fstack-protector -fstack-protector-all -iquote$(PROJECT_DIR)/external/com_github_krzyzanowskim_cryptoswift -iquote$(PROJECT_DIR)/bazel-out/ios-x86_64-min15.0-applebin_ios-ios_x86_64-dbg-STABLE-1/bin/external/com_github_krzyzanowskim_cryptoswift -iquote$(PROJECT_DIR) -iquote$(PROJECT_DIR)/bazel-out/ios-x86_64-min15.0-applebin_ios-ios_x86_64-dbg-STABLE-1/bin -O0 -fstack-protector -fstack-protector-all",
		"f": [
			"$(BAZEL_EXTERNAL)/com_github_krzyzanowskim_cryptoswift/CryptoSwift.xcframework/ios-arm64_i386_x86_64-simulator"
		],
		"s": [
			"$(BAZEL_OUT)/ios-x86_64-min15.0-applebin_ios-ios_x86_64-dbg-STABLE-1/bin/Lib"
		]
	},
	"x86_64-apple-ios-simulator iOSApp.app/iOSApp_ExecutableName": {
		"c": "-F$(PROJECT_DIR)/external/com_github_krzyzanowskim_cryptoswift/CryptoSwift.xcframework/ios-arm64_i386_x86_64-simulator -F$(PROJECT_DIR)/external/com_google_google_maps/GoogleMaps.xcframework/ios-arm64_x86_64-simulator -F$(PROJECT_DIR)/external/com_google_google_maps/GoogleMapsCore.xcframework/ios-arm64_x86_64-simulator -F$(PROJECT_DIR)/external/com_google_google_maps/GoogleMapsBase.xcframework/ios-arm64_x86_64-simulator -I$(PROJECT_DIR)/iOSApp/Source/CoreUtilsObjC -I$(PROJECT_DIR)/bazel-out/ios-x86_64-min15.0-applebin_ios-ios_x86_64-dbg-STABLE-1/bin/iOSApp/Source/CoreUtilsObjC -iquote$(PROJECT_DIR)/external/com_github_krzyzanowskim_cryptoswift -iquote$(PROJECT_DIR)/bazel-out/ios-x86_64-min15.0-applebin_ios-ios_x86_64-dbg-STABLE-1/bin/external/com_github_krzyzanowskim_cryptoswift -iquote$(PROJECT_DIR) -iquote$(PROJECT_DIR)/bazel-out/ios-x86_64-min15.0-applebin_ios-ios_x86_64-dbg-STABLE-1/bin -iquote$(PROJECT_DIR)/external/com_google_google_maps -iquote$(PROJECT_DIR)/bazel-out/ios-x86_64-min15.0-applebin_ios-ios_x86_64-dbg-STABLE-1/bin/external/com_google_google_maps -DNEEDS_QUOTES=Two\\ words -fmodule-map-file=$(PROJECT_DIR)/external/com_github_krzyzanowskim_cryptoswift/CryptoSwift.xcframework/ios-arm64_i386_x86_64-simulator/CryptoSwift.framework/Modules/module.modulemap -fmodule-map-file=$(PROJECT_DIR)/bazel-out/ios-x86_64-min15.0-applebin_ios-ios_x86_64-dbg-STABLE-1/bin/iOSApp/Source/CoreUtilsMixed/MixedAnswer/MixedAnswer_objc_modulemap.swift.modulemap -fmodule-map-file=$(PROJECT_DIR)/bazel-out/ios-x86_64-min15.0-applebin_ios-ios_x86_64-dbg-STABLE-1/bin/iOSApp/Source/CoreUtilsMixed/MixedAnswer/MixedAnswer_swift_modulemap.swift.modulemap -fmodule-map-file=$(PROJECT_DIR)/bazel-out/ios-x86_64-min15.0-applebin_ios-ios_x86_64-dbg-STABLE-1/bin/iOSApp/Source/CoreUtilsMixed/MixedAnswer/MixedAnswer_objc_modulemap-module.modulemap -fmodule-map-file=$(PROJECT_DIR)/bazel-out/ios-x86_64-min15.0-applebin_ios-ios_x86_64-dbg-STABLE-1/bin/iOSApp/Source/CoreUtilsObjC/CoreUtilsObjC.swift.modulemap -fmodule-map-file=$(PROJECT_DIR)/external/com_google_google_maps/GoogleMapsBase.xcframework/ios-arm64_x86_64-simulator/GoogleMapsBase.framework/Modules/module.modulemap -fmodule-map-file=$(PROJECT_DIR)/external/com_google_google_maps/GoogleMapsCore.xcframework/ios-arm64_x86_64-simulator/GoogleMapsCore.framework/Modules/module.modulemap -fmodule-map-file=$(PROJECT_DIR)/external/com_google_google_maps/GoogleMaps.xcframework/ios-arm64_x86_64-simulator/GoogleMaps.framework/Modules/module.modulemap -O0 -DDEBUG=1 -fstack-protector -fstack-protector-all -iquote$(PROJECT_DIR)/external/com_github_krzyzanowskim_cryptoswift -iquote$(PROJECT_DIR)/bazel-out/ios-x86_64-min15.0-applebin_ios-ios_x86_64-dbg-STABLE-1/bin/external/com_github_krzyzanowskim_cryptoswift -iquote$(PROJECT_DIR) -iquote$(PROJECT_DIR)/bazel-out/ios-x86_64-min15.0-applebin_ios-ios_x86_64-dbg-STABLE-1/bin -O0 -fstack-protector -fstack-protector-all -iquote$(PROJECT_DIR)/external/com_github_krzyzanowskim_cryptoswift -iquote$(PROJECT_DIR)/bazel-out/ios-x86_64-min15.0-applebin_ios-ios_x86_64-dbg-STABLE-1/bin/external/com_github_krzyzanowskim_cryptoswift -iquote$(PROJECT_DIR) -iquote$(PROJECT_DIR)/bazel-out/ios-x86_64-min15.0-applebin_ios-ios_x86_64-dbg-STABLE-1/bin -O0 -fstack-protector -fstack-protector-all -iquote$(PROJECT_DIR) -iquote$(PROJECT_DIR)/bazel-out/ios-x86_64-min15.0-applebin_ios-ios_x86_64-dbg-STABLE-1/bin -O0 -fstack-protector -fstack-protector-all",
		"f": [
			"$(BAZEL_EXTERNAL)/com_google_google_maps/GoogleMapsBase.xcframework/ios-arm64_x86_64-simulator",
			"$(BAZEL_EXTERNAL)/com_google_google_maps/GoogleMapsCore.xcframework/ios-arm64_x86_64-simulator",
			"$(BAZEL_EXTERNAL)/com_google_google_maps/GoogleMaps.xcframework/ios-arm64_x86_64-simulator",
			"$(BAZEL_EXTERNAL)/com_github_krzyzanowskim_cryptoswift/CryptoSwift.xcframework/ios-arm64_i386_x86_64-simulator"
		],
		"s": [
			"$(BAZEL_OUT)/ios-x86_64-min15.0-applebin_ios-ios_x86_64-dbg-STABLE-1/bin/UI",
			"$(BAZEL_OUT)/ios-x86_64-min15.0-applebin_ios-ios_x86_64-dbg-STABLE-1/bin/iOSApp/Source/CoreUtilsMixed/MixedAnswer",
			"$(BAZEL_OUT)/ios-x86_64-min15.0-applebin_ios-ios_x86_64-dbg-STABLE-1/bin/Lib"
		]
	},
	"x86_64-apple-ios-simulator iOSAppObjCUnitTestSuite.xctest/iOSAppObjCUnitTestSuite": {
		"c": "-F$(PROJECT_DIR)/external/com_github_krzyzanowskim_cryptoswift/CryptoSwift.xcframework/ios-arm64_i386_x86_64-simulator -F$(PROJECT_DIR)/external/com_google_google_maps/GoogleMaps.xcframework/ios-arm64_x86_64-simulator -F$(PROJECT_DIR)/external/com_google_google_maps/GoogleMapsCore.xcframework/ios-arm64_x86_64-simulator -F$(PROJECT_DIR)/external/com_google_google_maps/GoogleMapsBase.xcframework/ios-arm64_x86_64-simulator -I$(PROJECT_DIR)/iOSApp/Source/CoreUtilsObjC -I$(PROJECT_DIR)/bazel-out/ios-x86_64-min15.0-applebin_ios-ios_x86_64-dbg-STABLE-1/bin/iOSApp/Source/CoreUtilsObjC -iquote$(PROJECT_DIR)/external/com_github_krzyzanowskim_cryptoswift -iquote$(PROJECT_DIR)/bazel-out/ios-x86_64-min15.0-applebin_ios-ios_x86_64-dbg-STABLE-1/bin/external/com_github_krzyzanowskim_cryptoswift -iquote$(PROJECT_DIR) -iquote$(PROJECT_DIR)/bazel-out/ios-x86_64-min15.0-applebin_ios-ios_x86_64-dbg-STABLE-1/bin -iquote$(PROJECT_DIR)/external/com_google_google_maps -iquote$(PROJECT_DIR)/bazel-out/ios-x86_64-min15.0-applebin_ios-ios_x86_64-dbg-STABLE-1/bin/external/com_google_google_maps -DNEEDS_QUOTES=Two\\ words -fmodule-map-file=$(PROJECT_DIR)/external/com_github_krzyzanowskim_cryptoswift/CryptoSwift.xcframework/ios-arm64_i386_x86_64-simulator/CryptoSwift.framework/Modules/module.modulemap -fmodule-map-file=$(PROJECT_DIR)/bazel-out/ios-x86_64-min15.0-applebin_ios-ios_x86_64-dbg-STABLE-1/bin/iOSApp/Source/CoreUtilsMixed/MixedAnswer/MixedAnswer_objc_modulemap.swift.modulemap -fmodule-map-file=$(PROJECT_DIR)/bazel-out/ios-x86_64-min15.0-applebin_ios-ios_x86_64-dbg-STABLE-1/bin/iOSApp/Source/CoreUtilsMixed/MixedAnswer/MixedAnswer_swift_modulemap.swift.modulemap -fmodule-map-file=$(PROJECT_DIR)/bazel-out/ios-x86_64-min15.0-applebin_ios-ios_x86_64-dbg-STABLE-1/bin/iOSApp/Source/CoreUtilsMixed/MixedAnswer/MixedAnswer_objc_modulemap-module.modulemap -fmodule-map-file=$(PROJECT_DIR)/bazel-out/ios-x86_64-min15.0-applebin_ios-ios_x86_64-dbg-STABLE-1/bin/iOSApp/Source/CoreUtilsObjC/CoreUtilsObjC.swift.modulemap -fmodule-map-file=$(PROJECT_DIR)/external/com_google_google_maps/GoogleMapsBase.xcframework/ios-arm64_x86_64-simulator/GoogleMapsBase.framework/Modules/module.modulemap -fmodule-map-file=$(PROJECT_DIR)/external/com_google_google_maps/GoogleMapsCore.xcframework/ios-arm64_x86_64-simulator/GoogleMapsCore.framework/Modules/module.modulemap -fmodule-map-file=$(PROJECT_DIR)/external/com_google_google_maps/GoogleMaps.xcframework/ios-arm64_x86_64-simulator/GoogleMaps.framework/Modules/module.modulemap -O0 -DDEBUG=1 -fstack-protector -fstack-protector-all -iquote$(PROJECT_DIR)/external/com_github_krzyzanowskim_cryptoswift -iquote$(PROJECT_DIR)/bazel-out/ios-x86_64-min15.0-applebin_ios-ios_x86_64-dbg-STABLE-1/bin/external/com_github_krzyzanowskim_cryptoswift -iquote$(PROJECT_DIR) -iquote$(PROJECT_DIR)/bazel-out/ios-x86_64-min15.0-applebin_ios-ios_x86_64-dbg-STABLE-1/bin -O0 -fstack-protector -fstack-protector-all -iquote$(PROJECT_DIR)/external/com_github_krzyzanowskim_cryptoswift -iquote$(PROJECT_DIR)/bazel-out/ios-x86_64-min15.0-applebin_ios-ios_x86_64-dbg-STABLE-1/bin/external/com_github_krzyzanowskim_cryptoswift -iquote$(PROJECT_DIR) -iquote$(PROJECT_DIR)/bazel-out/ios-x86_64-min15.0-applebin_ios-ios_x86_64-dbg-STABLE-1/bin -O0 -fstack-protector -fstack-protector-all -iquote$(PROJECT_DIR) -iquote$(PROJECT_DIR)/bazel-out/ios-x86_64-min15.0-applebin_ios-ios_x86_64-dbg-STABLE-1/bin -O0 -fstack-protector -fstack-protector-all -iquote$(PROJECT_DIR) -iquote$(PROJECT_DIR)/bazel-out/ios-x86_64-min15.0-applebin_ios-ios_x86_64-dbg-STABLE-1/bin -O0 -fstack-protector -fstack-protector-all",
		"f": [
			"$(BAZEL_EXTERNAL)/com_google_google_maps/GoogleMapsBase.xcframework/ios-arm64_x86_64-simulator",
			"$(BAZEL_EXTERNAL)/com_google_google_maps/GoogleMapsCore.xcframework/ios-arm64_x86_64-simulator",
			"$(BAZEL_EXTERNAL)/com_google_google_maps/GoogleMaps.xcframework/ios-arm64_x86_64-simulator",
			"$(BAZEL_EXTERNAL)/com_github_krzyzanowskim_cryptoswift/CryptoSwift.xcframework/ios-arm64_i386_x86_64-simulator"
		],
		"s": [
			"$(BAZEL_OUT)/ios-x86_64-min15.0-applebin_ios-ios_x86_64-dbg-STABLE-1/bin/UI",
			"$(BAZEL_OUT)/ios-x86_64-min15.0-applebin_ios-ios_x86_64-dbg-STABLE-1/bin/iOSApp/Source/CoreUtilsMixed/MixedAnswer",
			"$(BAZEL_OUT)/ios-x86_64-min15.0-applebin_ios-ios_x86_64-dbg-STABLE-1/bin/Lib"
		]
	},
	"x86_64-apple-ios-simulator iOSAppObjCUnitTests.xctest/iOSAppObjCUnitTests": {
		"c": "-F$(PROJECT_DIR)/external/com_github_krzyzanowskim_cryptoswift/CryptoSwift.xcframework/ios-arm64_i386_x86_64-simulator -F$(PROJECT_DIR)/external/com_google_google_maps/GoogleMaps.xcframework/ios-arm64_x86_64-simulator -F$(PROJECT_DIR)/external/com_google_google_maps/GoogleMapsCore.xcframework/ios-arm64_x86_64-simulator -F$(PROJECT_DIR)/external/com_google_google_maps/GoogleMapsBase.xcframework/ios-arm64_x86_64-simulator -I$(PROJECT_DIR)/iOSApp/Source/CoreUtilsObjC -I$(PROJECT_DIR)/bazel-out/ios-x86_64-min15.0-applebin_ios-ios_x86_64-dbg-STABLE-1/bin/iOSApp/Source/CoreUtilsObjC -iquote$(PROJECT_DIR)/external/com_github_krzyzanowskim_cryptoswift -iquote$(PROJECT_DIR)/bazel-out/ios-x86_64-min15.0-applebin_ios-ios_x86_64-dbg-STABLE-1/bin/external/com_github_krzyzanowskim_cryptoswift -iquote$(PROJECT_DIR) -iquote$(PROJECT_DIR)/bazel-out/ios-x86_64-min15.0-applebin_ios-ios_x86_64-dbg-STABLE-1/bin -iquote$(PROJECT_DIR)/external/com_google_google_maps -iquote$(PROJECT_DIR)/bazel-out/ios-x86_64-min15.0-applebin_ios-ios_x86_64-dbg-STABLE-1/bin/external/com_google_google_maps -DNEEDS_QUOTES=Two\\ words -fmodule-map-file=$(PROJECT_DIR)/external/com_github_krzyzanowskim_cryptoswift/CryptoSwift.xcframework/ios-arm64_i386_x86_64-simulator/CryptoSwift.framework/Modules/module.modulemap -fmodule-map-file=$(PROJECT_DIR)/bazel-out/ios-x86_64-min15.0-applebin_ios-ios_x86_64-dbg-STABLE-1/bin/iOSApp/Source/CoreUtilsMixed/MixedAnswer/MixedAnswer_objc_modulemap.swift.modulemap -fmodule-map-file=$(PROJECT_DIR)/bazel-out/ios-x86_64-min15.0-applebin_ios-ios_x86_64-dbg-STABLE-1/bin/iOSApp/Source/CoreUtilsMixed/MixedAnswer/MixedAnswer_swift_modulemap.swift.modulemap -fmodule-map-file=$(PROJECT_DIR)/bazel-out/ios-x86_64-min15.0-applebin_ios-ios_x86_64-dbg-STABLE-1/bin/iOSApp/Source/CoreUtilsMixed/MixedAnswer/MixedAnswer_objc_modulemap-module.modulemap -fmodule-map-file=$(PROJECT_DIR)/bazel-out/ios-x86_64-min15.0-applebin_ios-ios_x86_64-dbg-STABLE-1/bin/iOSApp/Source/CoreUtilsObjC/CoreUtilsObjC.swift.modulemap -fmodule-map-file=$(PROJECT_DIR)/external/com_google_google_maps/GoogleMapsBase.xcframework/ios-arm64_x86_64-simulator/GoogleMapsBase.framework/Modules/module.modulemap -fmodule-map-file=$(PROJECT_DIR)/external/com_google_google_maps/GoogleMapsCore.xcframework/ios-arm64_x86_64-simulator/GoogleMapsCore.framework/Modules/module.modulemap -fmodule-map-file=$(PROJECT_DIR)/external/com_google_google_maps/GoogleMaps.xcframework/ios-arm64_x86_64-simulator/GoogleMaps.framework/Modules/module.modulemap -O0 -DDEBUG=1 -fstack-protector -fstack-protector-all -iquote$(PROJECT_DIR)/external/com_github_krzyzanowskim_cryptoswift -iquote$(PROJECT_DIR)/bazel-out/ios-x86_64-min15.0-applebin_ios-ios_x86_64-dbg-STABLE-1/bin/external/com_github_krzyzanowskim_cryptoswift -iquote$(PROJECT_DIR) -iquote$(PROJECT_DIR)/bazel-out/ios-x86_64-min15.0-applebin_ios-ios_x86_64-dbg-STABLE-1/bin -O0 -fstack-protector -fstack-protector-all -iquote$(PROJECT_DIR)/external/com_github_krzyzanowskim_cryptoswift -iquote$(PROJECT_DIR)/bazel-out/ios-x86_64-min15.0-applebin_ios-ios_x86_64-dbg-STABLE-1/bin/external/com_github_krzyzanowskim_cryptoswift -iquote$(PROJECT_DIR) -iquote$(PROJECT_DIR)/bazel-out/ios-x86_64-min15.0-applebin_ios-ios_x86_64-dbg-STABLE-1/bin -O0 -fstack-protector -fstack-protector-all -iquote$(PROJECT_DIR) -iquote$(PROJECT_DIR)/bazel-out/ios-x86_64-min15.0-applebin_ios-ios_x86_64-dbg-STABLE-1/bin -O0 -fstack-protector -fstack-protector-all -iquote$(PROJECT_DIR) -iquote$(PROJECT_DIR)/bazel-out/ios-x86_64-min15.0-applebin_ios-ios_x86_64-dbg-STABLE-1/bin -O0 -fstack-protector -fstack-protector-all",
		"f": [
			"$(BAZEL_EXTERNAL)/com_google_google_maps/GoogleMapsBase.xcframework/ios-arm64_x86_64-simulator",
			"$(BAZEL_EXTERNAL)/com_google_google_maps/GoogleMapsCore.xcframework/ios-arm64_x86_64-simulator",
			"$(BAZEL_EXTERNAL)/com_google_google_maps/GoogleMaps.xcframework/ios-arm64_x86_64-simulator",
			"$(BAZEL_EXTERNAL)/com_github_krzyzanowskim_cryptoswift/CryptoSwift.xcframework/ios-arm64_i386_x86_64-simulator"
		],
		"s": [
			"$(BAZEL_OUT)/ios-x86_64-min15.0-applebin_ios-ios_x86_64-dbg-STABLE-1/bin/UI",
			"$(BAZEL_OUT)/ios-x86_64-min15.0-applebin_ios-ios_x86_64-dbg-STABLE-1/bin/iOSApp/Source/CoreUtilsMixed/MixedAnswer",
			"$(BAZEL_OUT)/ios-x86_64-min15.0-applebin_ios-ios_x86_64-dbg-STABLE-1/bin/Lib"
		]
	},
	"x86_64-apple-ios-simulator iOSAppSwiftUnitTestSuite.xctest/iOSAppSwiftUnitTestSuite": {
		"c": "-F$(PROJECT_DIR)/external/com_github_krzyzanowskim_cryptoswift/CryptoSwift.xcframework/ios-arm64_i386_x86_64-simulator -F$(PROJECT_DIR)/external/com_google_google_maps/GoogleMaps.xcframework/ios-arm64_x86_64-simulator -F$(PROJECT_DIR)/external/com_google_google_maps/GoogleMapsCore.xcframework/ios-arm64_x86_64-simulator -F$(PROJECT_DIR)/external/com_google_google_maps/GoogleMapsBase.xcframework/ios-arm64_x86_64-simulator -I$(PROJECT_DIR)/iOSApp/Source/CoreUtilsObjC -I$(PROJECT_DIR)/bazel-out/ios-x86_64-min15.0-applebin_ios-ios_x86_64-dbg-STABLE-1/bin/iOSApp/Source/CoreUtilsObjC -iquote$(PROJECT_DIR)/external/com_github_krzyzanowskim_cryptoswift -iquote$(PROJECT_DIR)/bazel-out/ios-x86_64-min15.0-applebin_ios-ios_x86_64-dbg-STABLE-1/bin/external/com_github_krzyzanowskim_cryptoswift -iquote$(PROJECT_DIR) -iquote$(PROJECT_DIR)/bazel-out/ios-x86_64-min15.0-applebin_ios-ios_x86_64-dbg-STABLE-1/bin -iquote$(PROJECT_DIR)/external/com_google_google_maps -iquote$(PROJECT_DIR)/bazel-out/ios-x86_64-min15.0-applebin_ios-ios_x86_64-dbg-STABLE-1/bin/external/com_google_google_maps -iquote$(PROJECT_DIR)/external/FXPageControl -iquote$(PROJECT_DIR)/bazel-out/ios-x86_64-min15.0-applebin_ios-ios_x86_64-dbg-STABLE-1/bin/external/FXPageControl -DNEEDS_QUOTES=Two\\ words -DAWESOME -fmodule-map-file=$(PROJECT_DIR)/external/com_github_krzyzanowskim_cryptoswift/CryptoSwift.xcframework/ios-arm64_i386_x86_64-simulator/CryptoSwift.framework/Modules/module.modulemap -fmodule-map-file=$(PROJECT_DIR)/bazel-out/ios-x86_64-min15.0-applebin_ios-ios_x86_64-dbg-STABLE-1/bin/iOSApp/Source/CoreUtilsMixed/MixedAnswer/MixedAnswer_objc_modulemap.swift.modulemap -fmodule-map-file=$(PROJECT_DIR)/bazel-out/ios-x86_64-min15.0-applebin_ios-ios_x86_64-dbg-STABLE-1/bin/iOSApp/Source/CoreUtilsMixed/MixedAnswer/MixedAnswer_swift_modulemap.swift.modulemap -fmodule-map-file=$(PROJECT_DIR)/bazel-out/ios-x86_64-min15.0-applebin_ios-ios_x86_64-dbg-STABLE-1/bin/iOSApp/Source/CoreUtilsMixed/MixedAnswer/MixedAnswer_objc_modulemap-module.modulemap -fmodule-map-file=$(PROJECT_DIR)/bazel-out/ios-x86_64-min15.0-applebin_ios-ios_x86_64-dbg-STABLE-1/bin/iOSApp/Source/CoreUtilsObjC/CoreUtilsObjC.swift.modulemap -fmodule-map-file=$(PROJECT_DIR)/external/com_google_google_maps/GoogleMapsBase.xcframework/ios-arm64_x86_64-simulator/GoogleMapsBase.framework/Modules/module.modulemap -fmodule-map-file=$(PROJECT_DIR)/external/com_google_google_maps/GoogleMapsCore.xcframework/ios-arm64_x86_64-simulator/GoogleMapsCore.framework/Modules/module.modulemap -fmodule-map-file=$(PROJECT_DIR)/external/com_google_google_maps/GoogleMaps.xcframework/ios-arm64_x86_64-simulator/GoogleMaps.framework/Modules/module.modulemap -fmodule-map-file=$(PROJECT_DIR)/bazel-out/ios-x86_64-min15.0-applebin_ios-ios_x86_64-dbg-STABLE-1/bin/external/FXPageControl/FXPageControl.swift.modulemap -fmodule-map-file=$(PROJECT_DIR)/bazel-out/ios-x86_64-min15.0-applebin_ios-ios_x86_64-dbg-STABLE-1/bin/iOSApp/Source/Utils/Utils.swift.modulemap -fmodule-map-file=$(PROJECT_DIR)/bazel-out/ios-x86_64-min15.0-applebin_ios-ios_x86_64-dbg-STABLE-1/bin/iOSApp/Test/TestingUtils/TestingUtils.swift.modulemap -O0 -DDEBUG=1 -fstack-protector -fstack-protector-all -iquote$(PROJECT_DIR)/external/com_github_krzyzanowskim_cryptoswift -iquote$(PROJECT_DIR)/bazel-out/ios-x86_64-min15.0-applebin_ios-ios_x86_64-dbg-STABLE-1/bin/external/com_github_krzyzanowskim_cryptoswift -iquote$(PROJECT_DIR) -iquote$(PROJECT_DIR)/bazel-out/ios-x86_64-min15.0-applebin_ios-ios_x86_64-dbg-STABLE-1/bin -iquote$(PROJECT_DIR)/external/com_google_google_maps -iquote$(PROJECT_DIR)/bazel-out/ios-x86_64-min15.0-applebin_ios-ios_x86_64-dbg-STABLE-1/bin/external/com_google_google_maps -O0 -fstack-protector -fstack-protector-all -iquote$(PROJECT_DIR)/external/com_github_krzyzanowskim_cryptoswift -iquote$(PROJECT_DIR)/bazel-out/ios-x86_64-min15.0-applebin_ios-ios_x86_64-dbg-STABLE-1/bin/external/com_github_krzyzanowskim_cryptoswift -iquote$(PROJECT_DIR) -iquote$(PROJECT_DIR)/bazel-out/ios-x86_64-min15.0-applebin_ios-ios_x86_64-dbg-STABLE-1/bin -O0 -fstack-protector -fstack-protector-all -iquote$(PROJECT_DIR)/external/com_github_krzyzanowskim_cryptoswift -iquote$(PROJECT_DIR)/bazel-out/ios-x86_64-min15.0-applebin_ios-ios_x86_64-dbg-STABLE-1/bin/external/com_github_krzyzanowskim_cryptoswift -iquote$(PROJECT_DIR) -iquote$(PROJECT_DIR)/bazel-out/ios-x86_64-min15.0-applebin_ios-ios_x86_64-dbg-STABLE-1/bin -O0 -fstack-protector -fstack-protector-all -iquote$(PROJECT_DIR) -iquote$(PROJECT_DIR)/bazel-out/ios-x86_64-min15.0-applebin_ios-ios_x86_64-dbg-STABLE-1/bin -O0 -fstack-protector -fstack-protector-all -iquote$(PROJECT_DIR) -iquote$(PROJECT_DIR)/bazel-out/ios-x86_64-min15.0-applebin_ios-ios_x86_64-dbg-STABLE-1/bin -O0 -fstack-protector -fstack-protector-all",
		"f": [
			"$(BAZEL_EXTERNAL)/com_google_google_maps/GoogleMapsBase.xcframework/ios-arm64_x86_64-simulator",
			"$(BAZEL_EXTERNAL)/com_google_google_maps/GoogleMapsCore.xcframework/ios-arm64_x86_64-simulator",
			"$(BAZEL_EXTERNAL)/com_google_google_maps/GoogleMaps.xcframework/ios-arm64_x86_64-simulator",
			"$(BAZEL_EXTERNAL)/com_github_krzyzanowskim_cryptoswift/CryptoSwift.xcframework/ios-arm64_i386_x86_64-simulator"
		],
		"s": [
			"$(BAZEL_OUT)/ios-x86_64-min15.0-applebin_ios-ios_x86_64-dbg-STABLE-1/bin/iOSApp/Source",
			"$(BAZEL_OUT)/ios-x86_64-min15.0-applebin_ios-ios_x86_64-dbg-STABLE-1/bin/iOSApp/Test/TestingUtils",
			"$(BAZEL_OUT)/ios-x86_64-min15.0-applebin_ios-ios_x86_64-dbg-STABLE-1/bin/UI",
			"$(BAZEL_OUT)/ios-x86_64-min15.0-applebin_ios-ios_x86_64-dbg-STABLE-1/bin/iOSApp/Source/CoreUtilsMixed/MixedAnswer",
			"$(BAZEL_OUT)/ios-x86_64-min15.0-applebin_ios-ios_x86_64-dbg-STABLE-1/bin/Lib"
		]
	},
	"x86_64-apple-ios-simulator iOSAppSwiftUnitTests.xctest/iOSAppSwiftUnitTests": {
		"c": "-F$(PROJECT_DIR)/external/com_github_krzyzanowskim_cryptoswift/CryptoSwift.xcframework/ios-arm64_i386_x86_64-simulator -F$(PROJECT_DIR)/external/com_google_google_maps/GoogleMaps.xcframework/ios-arm64_x86_64-simulator -F$(PROJECT_DIR)/external/com_google_google_maps/GoogleMapsCore.xcframework/ios-arm64_x86_64-simulator -F$(PROJECT_DIR)/external/com_google_google_maps/GoogleMapsBase.xcframework/ios-arm64_x86_64-simulator -I$(PROJECT_DIR)/iOSApp/Source/CoreUtilsObjC -I$(PROJECT_DIR)/bazel-out/ios-x86_64-min15.0-applebin_ios-ios_x86_64-dbg-STABLE-1/bin/iOSApp/Source/CoreUtilsObjC -iquote$(PROJECT_DIR)/external/com_github_krzyzanowskim_cryptoswift -iquote$(PROJECT_DIR)/bazel-out/ios-x86_64-min15.0-applebin_ios-ios_x86_64-dbg-STABLE-1/bin/external/com_github_krzyzanowskim_cryptoswift -iquote$(PROJECT_DIR) -iquote$(PROJECT_DIR)/bazel-out/ios-x86_64-min15.0-applebin_ios-ios_x86_64-dbg-STABLE-1/bin -iquote$(PROJECT_DIR)/external/com_google_google_maps -iquote$(PROJECT_DIR)/bazel-out/ios-x86_64-min15.0-applebin_ios-ios_x86_64-dbg-STABLE-1/bin/external/com_google_google_maps -iquote$(PROJECT_DIR)/external/FXPageControl -iquote$(PROJECT_DIR)/bazel-out/ios-x86_64-min15.0-applebin_ios-ios_x86_64-dbg-STABLE-1/bin/external/FXPageControl -DNEEDS_QUOTES=Two\\ words -DAWESOME -fmodule-map-file=$(PROJECT_DIR)/external/com_github_krzyzanowskim_cryptoswift/CryptoSwift.xcframework/ios-arm64_i386_x86_64-simulator/CryptoSwift.framework/Modules/module.modulemap -fmodule-map-file=$(PROJECT_DIR)/bazel-out/ios-x86_64-min15.0-applebin_ios-ios_x86_64-dbg-STABLE-1/bin/iOSApp/Source/CoreUtilsMixed/MixedAnswer/MixedAnswer_objc_modulemap.swift.modulemap -fmodule-map-file=$(PROJECT_DIR)/bazel-out/ios-x86_64-min15.0-applebin_ios-ios_x86_64-dbg-STABLE-1/bin/iOSApp/Source/CoreUtilsMixed/MixedAnswer/MixedAnswer_swift_modulemap.swift.modulemap -fmodule-map-file=$(PROJECT_DIR)/bazel-out/ios-x86_64-min15.0-applebin_ios-ios_x86_64-dbg-STABLE-1/bin/iOSApp/Source/CoreUtilsMixed/MixedAnswer/MixedAnswer_objc_modulemap-module.modulemap -fmodule-map-file=$(PROJECT_DIR)/bazel-out/ios-x86_64-min15.0-applebin_ios-ios_x86_64-dbg-STABLE-1/bin/iOSApp/Source/CoreUtilsObjC/CoreUtilsObjC.swift.modulemap -fmodule-map-file=$(PROJECT_DIR)/external/com_google_google_maps/GoogleMapsBase.xcframework/ios-arm64_x86_64-simulator/GoogleMapsBase.framework/Modules/module.modulemap -fmodule-map-file=$(PROJECT_DIR)/external/com_google_google_maps/GoogleMapsCore.xcframework/ios-arm64_x86_64-simulator/GoogleMapsCore.framework/Modules/module.modulemap -fmodule-map-file=$(PROJECT_DIR)/external/com_google_google_maps/GoogleMaps.xcframework/ios-arm64_x86_64-simulator/GoogleMaps.framework/Modules/module.modulemap -fmodule-map-file=$(PROJECT_DIR)/bazel-out/ios-x86_64-min15.0-applebin_ios-ios_x86_64-dbg-STABLE-1/bin/external/FXPageControl/FXPageControl.swift.modulemap -fmodule-map-file=$(PROJECT_DIR)/bazel-out/ios-x86_64-min15.0-applebin_ios-ios_x86_64-dbg-STABLE-1/bin/iOSApp/Source/Utils/Utils.swift.modulemap -fmodule-map-file=$(PROJECT_DIR)/bazel-out/ios-x86_64-min15.0-applebin_ios-ios_x86_64-dbg-STABLE-1/bin/iOSApp/Test/TestingUtils/TestingUtils.swift.modulemap -O0 -DDEBUG=1 -fstack-protector -fstack-protector-all -iquote$(PROJECT_DIR)/external/com_github_krzyzanowskim_cryptoswift -iquote$(PROJECT_DIR)/bazel-out/ios-x86_64-min15.0-applebin_ios-ios_x86_64-dbg-STABLE-1/bin/external/com_github_krzyzanowskim_cryptoswift -iquote$(PROJECT_DIR) -iquote$(PROJECT_DIR)/bazel-out/ios-x86_64-min15.0-applebin_ios-ios_x86_64-dbg-STABLE-1/bin -iquote$(PROJECT_DIR)/external/com_google_google_maps -iquote$(PROJECT_DIR)/bazel-out/ios-x86_64-min15.0-applebin_ios-ios_x86_64-dbg-STABLE-1/bin/external/com_google_google_maps -O0 -fstack-protector -fstack-protector-all -iquote$(PROJECT_DIR)/external/com_github_krzyzanowskim_cryptoswift -iquote$(PROJECT_DIR)/bazel-out/ios-x86_64-min15.0-applebin_ios-ios_x86_64-dbg-STABLE-1/bin/external/com_github_krzyzanowskim_cryptoswift -iquote$(PROJECT_DIR) -iquote$(PROJECT_DIR)/bazel-out/ios-x86_64-min15.0-applebin_ios-ios_x86_64-dbg-STABLE-1/bin -O0 -fstack-protector -fstack-protector-all -iquote$(PROJECT_DIR)/external/com_github_krzyzanowskim_cryptoswift -iquote$(PROJECT_DIR)/bazel-out/ios-x86_64-min15.0-applebin_ios-ios_x86_64-dbg-STABLE-1/bin/external/com_github_krzyzanowskim_cryptoswift -iquote$(PROJECT_DIR) -iquote$(PROJECT_DIR)/bazel-out/ios-x86_64-min15.0-applebin_ios-ios_x86_64-dbg-STABLE-1/bin -O0 -fstack-protector -fstack-protector-all -iquote$(PROJECT_DIR) -iquote$(PROJECT_DIR)/bazel-out/ios-x86_64-min15.0-applebin_ios-ios_x86_64-dbg-STABLE-1/bin -O0 -fstack-protector -fstack-protector-all -iquote$(PROJECT_DIR) -iquote$(PROJECT_DIR)/bazel-out/ios-x86_64-min15.0-applebin_ios-ios_x86_64-dbg-STABLE-1/bin -O0 -fstack-protector -fstack-protector-all",
		"f": [
			"$(BAZEL_EXTERNAL)/com_google_google_maps/GoogleMapsBase.xcframework/ios-arm64_x86_64-simulator",
			"$(BAZEL_EXTERNAL)/com_google_google_maps/GoogleMapsCore.xcframework/ios-arm64_x86_64-simulator",
			"$(BAZEL_EXTERNAL)/com_google_google_maps/GoogleMaps.xcframework/ios-arm64_x86_64-simulator",
			"$(BAZEL_EXTERNAL)/com_github_krzyzanowskim_cryptoswift/CryptoSwift.xcframework/ios-arm64_i386_x86_64-simulator"
		],
		"s": [
			"$(BAZEL_OUT)/ios-x86_64-min15.0-applebin_ios-ios_x86_64-dbg-STABLE-1/bin/iOSApp/Source",
			"$(BAZEL_OUT)/ios-x86_64-min15.0-applebin_ios-ios_x86_64-dbg-STABLE-1/bin/iOSApp/Test/TestingUtils",
			"$(BAZEL_OUT)/ios-x86_64-min15.0-applebin_ios-ios_x86_64-dbg-STABLE-1/bin/UI",
			"$(BAZEL_OUT)/ios-x86_64-min15.0-applebin_ios-ios_x86_64-dbg-STABLE-1/bin/iOSApp/Source/CoreUtilsMixed/MixedAnswer",
			"$(BAZEL_OUT)/ios-x86_64-min15.0-applebin_ios-ios_x86_64-dbg-STABLE-1/bin/Lib"
		]
	},
	"x86_64-apple-ios-simulator iOSAppUITestSuite.xctest/iOSAppUITestSuite": {
		"c": "-iquote$(PROJECT_DIR) -iquote$(PROJECT_DIR)/bazel-out/ios-x86_64-min15.0-applebin_ios-ios_x86_64-dbg-STABLE-1/bin -O0 -DDEBUG=1 -fstack-protector -fstack-protector-all"
	},
	"x86_64-apple-ios-simulator iOSAppUITests.xctest/iOSAppUITests": {
		"c": "-iquote$(PROJECT_DIR) -iquote$(PROJECT_DIR)/bazel-out/ios-x86_64-min15.0-applebin_ios-ios_x86_64-dbg-STABLE-1/bin -O0 -DDEBUG=1 -fstack-protector -fstack-protector-all"
	},
	"x86_64-apple-macosx CommandLineTool": {
		"c": "-F$(PROJECT_DIR)/external/examples_command_line_external -I$(SDKROOT)/usr/include/uuid -iquote$(PROJECT_DIR) -iquote$(PROJECT_DIR)/bazel-out/macos-x86_64-min11.0-applebin_macos-darwin_x86_64-dbg-STABLE-33/bin -iquote$(PROJECT_DIR)/external/examples_command_line_external -iquote$(PROJECT_DIR)/bazel-out/macos-x86_64-min11.0-applebin_macos-darwin_x86_64-dbg-STABLE-33/bin/external/examples_command_line_external -DSECRET_3=\"Hello\" -DSECRET_2=\"World!\" -fmodule-map-file=$(PROJECT_DIR)/bazel-out/macos-x86_64-min11.0-applebin_macos-darwin_x86_64-dbg-STABLE-33/bin/CommandLine/CommandLineToolLib/lib_impl.swift.modulemap -fmodule-map-file=$(PROJECT_DIR)/CommandLine/swift_c_module/c_lib.modulemap -fmodule-map-file=$(PROJECT_DIR)/external/examples_command_line_external/ExternalFramework.framework/Modules/module.modulemap -fmodule-map-file=$(PROJECT_DIR)/bazel-out/macos-x86_64-min11.0-applebin_macos-darwin_x86_64-dbg-STABLE-33/bin/external/examples_command_line_external/Library.swift.modulemap -fmodule-map-file=$(PROJECT_DIR)/bazel-out/macos-x86_64-min11.0-applebin_macos-darwin_x86_64-dbg-STABLE-33/bin/CommandLine/CommandLineToolLib/private_lib.swift.modulemap -O0 -DDEBUG=1 -fstack-protector -fstack-protector-all -iquote$(PROJECT_DIR) -iquote$(PROJECT_DIR)/bazel-out/macos-x86_64-min11.0-applebin_macos-darwin_x86_64-dbg-STABLE-33/bin -O0 -fstack-protector -fstack-protector-all",
		"f": [
			"$(BAZEL_EXTERNAL)/examples_command_line_external"
		],
		"s": [
			"$(BAZEL_OUT)/macos-x86_64-min11.0-applebin_macos-darwin_x86_64-dbg-STABLE-33/bin/CommandLine/CommandLineToolLib"
		]
	},
	"x86_64-apple-macosx CommandLineToolTests.xctest/Contents/MacOS/CommandLineToolTests": {
		"c": "-F$(PROJECT_DIR)/external/examples_command_line_external -I$(SDKROOT)/usr/include/uuid -iquote$(PROJECT_DIR) -iquote$(PROJECT_DIR)/bazel-out/macos-x86_64-min11.0-applebin_macos-darwin_x86_64-dbg-STABLE-33/bin -iquote$(PROJECT_DIR)/external/examples_command_line_external -iquote$(PROJECT_DIR)/bazel-out/macos-x86_64-min11.0-applebin_macos-darwin_x86_64-dbg-STABLE-33/bin/external/examples_command_line_external -DSECRET_3=\"Hello\" -DSECRET_2=\"World!\" -fmodule-map-file=$(PROJECT_DIR)/bazel-out/macos-x86_64-min11.0-applebin_macos-darwin_x86_64-dbg-STABLE-33/bin/CommandLine/CommandLineToolLib/lib_impl.swift.modulemap -fmodule-map-file=$(PROJECT_DIR)/CommandLine/swift_c_module/c_lib.modulemap -fmodule-map-file=$(PROJECT_DIR)/external/examples_command_line_external/ExternalFramework.framework/Modules/module.modulemap -fmodule-map-file=$(PROJECT_DIR)/bazel-out/macos-x86_64-min11.0-applebin_macos-darwin_x86_64-dbg-STABLE-33/bin/external/examples_command_line_external/Library.swift.modulemap -fmodule-map-file=$(PROJECT_DIR)/bazel-out/macos-x86_64-min11.0-applebin_macos-darwin_x86_64-dbg-STABLE-33/bin/CommandLine/CommandLineToolLib/lib_swift.swift.modulemap -O0 -DDEBUG=1 -fstack-protector -fstack-protector-all -iquote$(PROJECT_DIR) -iquote$(PROJECT_DIR)/bazel-out/macos-x86_64-min11.0-applebin_macos-darwin_x86_64-dbg-STABLE-33/bin -iquote$(PROJECT_DIR)/external/examples_command_line_external -iquote$(PROJECT_DIR)/bazel-out/macos-x86_64-min11.0-applebin_macos-darwin_x86_64-dbg-STABLE-33/bin/external/examples_command_line_external -fmodule-map-file=$(PROJECT_DIR)/bazel-out/macos-x86_64-min11.0-applebin_macos-darwin_x86_64-dbg-STABLE-33/bin/CommandLine/CommandLineToolLib/private_lib.swift.modulemap -O0 -fstack-protector -fstack-protector-all -iquote$(PROJECT_DIR) -iquote$(PROJECT_DIR)/bazel-out/macos-x86_64-min11.0-applebin_macos-darwin_x86_64-dbg-STABLE-33/bin -O0 -fstack-protector -fstack-protector-all",
		"f": [
			"$(BAZEL_EXTERNAL)/examples_command_line_external"
		],
		"s": [
			"$(BAZEL_OUT)/macos-x86_64-min11.0-applebin_macos-darwin_x86_64-dbg-STABLE-33/bin/CommandLine/CommandLineToolLib"
		]
	},
	"x86_64-apple-macosx macOSApp.app/Contents/MacOS/macOSApp": {
		"c": "-F$(PROJECT_DIR)/macOSApp/third_party -iquote$(PROJECT_DIR) -iquote$(PROJECT_DIR)/bazel-out/macos-x86_64-min12.0-applebin_macos-darwin_x86_64-dbg-STABLE-29/bin -fmodule-map-file=$(PROJECT_DIR)/macOSApp/third_party/ExampleFramework.framework/Modules/module.modulemap -O0 -DDEBUG=1 -fstack-protector -fstack-protector-all",
		"f": [
			"$(SRCROOT)/macOSApp/third_party"
		]
	},
	"x86_64-apple-macosx macOSAppUITests.xctest/Contents/MacOS/macOSAppUITests": {
		"c": "-iquote$(PROJECT_DIR) -iquote$(PROJECT_DIR)/bazel-out/macos-x86_64-min12.0-applebin_macos-darwin_x86_64-dbg-STABLE-29/bin -O0 -DDEBUG=1 -fstack-protector -fstack-protector-all"
	},
	"x86_64-apple-macosx tool.binary": {
		"c": "-F$(PROJECT_DIR)/external/examples_command_line_external -I$(SDKROOT)/usr/include/uuid -iquote$(PROJECT_DIR) -iquote$(PROJECT_DIR)/bazel-out/macos-x86_64-min11.0-applebin_macos-darwin_x86_64-dbg-STABLE-35/bin -iquote$(PROJECT_DIR)/external/examples_command_line_external -iquote$(PROJECT_DIR)/bazel-out/macos-x86_64-min11.0-applebin_macos-darwin_x86_64-dbg-STABLE-35/bin/external/examples_command_line_external -DSECRET_3=\"Hello\" -DSECRET_2=\"World!\" -fmodule-map-file=$(PROJECT_DIR)/bazel-out/macos-x86_64-min11.0-applebin_macos-darwin_x86_64-dbg-STABLE-35/bin/CommandLine/CommandLineToolLib/lib_impl.swift.modulemap -fmodule-map-file=$(PROJECT_DIR)/CommandLine/swift_c_module/c_lib.modulemap -fmodule-map-file=$(PROJECT_DIR)/external/examples_command_line_external/ExternalFramework.framework/Modules/module.modulemap -fmodule-map-file=$(PROJECT_DIR)/bazel-out/macos-x86_64-min11.0-applebin_macos-darwin_x86_64-dbg-STABLE-35/bin/external/examples_command_line_external/Library.swift.modulemap -fmodule-map-file=$(PROJECT_DIR)/bazel-out/macos-x86_64-min11.0-applebin_macos-darwin_x86_64-dbg-STABLE-35/bin/CommandLine/CommandLineToolLib/private_lib.swift.modulemap -O0 -DDEBUG=1 -fstack-protector -fstack-protector-all -iquote$(PROJECT_DIR) -iquote$(PROJECT_DIR)/bazel-out/macos-x86_64-min11.0-applebin_macos-darwin_x86_64-dbg-STABLE-35/bin -O0 -fstack-protector -fstack-protector-all",
		"f": [
			"$(BAZEL_EXTERNAL)/examples_command_line_external"
		],
		"s": [
			"$(BAZEL_OUT)/macos-x86_64-min11.0-applebin_macos-darwin_x86_64-dbg-STABLE-35/bin/CommandLine/CommandLineToolLib"
		]
	},
	"x86_64-apple-tvos-simulator Lib.framework/Lib": {
		"c": "-F$(PROJECT_DIR)/external/com_github_krzyzanowskim_cryptoswift/CryptoSwift.xcframework/tvos-arm64_x86_64-simulator -iquote$(PROJECT_DIR)/external/com_github_krzyzanowskim_cryptoswift -iquote$(PROJECT_DIR)/bazel-out/tvos-x86_64-min15.0-applebin_tvos-tvos_x86_64-dbg-STABLE-3/bin/external/com_github_krzyzanowskim_cryptoswift -iquote$(PROJECT_DIR) -iquote$(PROJECT_DIR)/bazel-out/tvos-x86_64-min15.0-applebin_tvos-tvos_x86_64-dbg-STABLE-3/bin -fmodule-map-file=$(PROJECT_DIR)/external/com_github_krzyzanowskim_cryptoswift/CryptoSwift.xcframework/tvos-arm64_x86_64-simulator/CryptoSwift.framework/Modules/module.modulemap -O0 -DDEBUG=1 -fstack-protector -fstack-protector-all",
		"f": [
			"$(BAZEL_EXTERNAL)/com_github_krzyzanowskim_cryptoswift/CryptoSwift.xcframework/tvos-arm64_x86_64-simulator"
		]
	},
	"x86_64-apple-tvos-simulator LibFramework.tvOS.framework/LibFramework.tvOS": {
		"c": "-F$(PROJECT_DIR)/external/com_github_krzyzanowskim_cryptoswift/CryptoSwift.xcframework/tvos-arm64_x86_64-simulator -iquote$(PROJECT_DIR)/external/com_github_krzyzanowskim_cryptoswift -iquote$(PROJECT_DIR)/bazel-out/tvos-x86_64-min15.0-applebin_tvos-tvos_x86_64-dbg-STABLE-3/bin/external/com_github_krzyzanowskim_cryptoswift -iquote$(PROJECT_DIR) -iquote$(PROJECT_DIR)/bazel-out/tvos-x86_64-min15.0-applebin_tvos-tvos_x86_64-dbg-STABLE-3/bin -fmodule-map-file=$(PROJECT_DIR)/external/com_github_krzyzanowskim_cryptoswift/CryptoSwift.xcframework/tvos-arm64_x86_64-simulator/CryptoSwift.framework/Modules/module.modulemap -O0 -DDEBUG=1 -fstack-protector -fstack-protector-all",
		"f": [
			"$(BAZEL_EXTERNAL)/com_github_krzyzanowskim_cryptoswift/CryptoSwift.xcframework/tvos-arm64_x86_64-simulator"
		]
	},
	"x86_64-apple-tvos-simulator UIFramework.tvOS.framework/UIFramework.tvOS": {
		"c": "-F$(PROJECT_DIR)/external/com_github_krzyzanowskim_cryptoswift/CryptoSwift.xcframework/tvos-arm64_x86_64-simulator -iquote$(PROJECT_DIR)/external/com_github_krzyzanowskim_cryptoswift -iquote$(PROJECT_DIR)/bazel-out/tvos-x86_64-min15.0-applebin_tvos-tvos_x86_64-dbg-STABLE-3/bin/external/com_github_krzyzanowskim_cryptoswift -iquote$(PROJECT_DIR) -iquote$(PROJECT_DIR)/bazel-out/tvos-x86_64-min15.0-applebin_tvos-tvos_x86_64-dbg-STABLE-3/bin -fmodule-map-file=$(PROJECT_DIR)/external/com_github_krzyzanowskim_cryptoswift/CryptoSwift.xcframework/tvos-arm64_x86_64-simulator/CryptoSwift.framework/Modules/module.modulemap -O0 -DDEBUG=1 -fstack-protector -fstack-protector-all -iquote$(PROJECT_DIR)/external/com_github_krzyzanowskim_cryptoswift -iquote$(PROJECT_DIR)/bazel-out/tvos-x86_64-min15.0-applebin_tvos-tvos_x86_64-dbg-STABLE-3/bin/external/com_github_krzyzanowskim_cryptoswift -iquote$(PROJECT_DIR) -iquote$(PROJECT_DIR)/bazel-out/tvos-x86_64-min15.0-applebin_tvos-tvos_x86_64-dbg-STABLE-3/bin -O0 -fstack-protector -fstack-protector-all",
		"f": [
			"$(BAZEL_EXTERNAL)/com_github_krzyzanowskim_cryptoswift/CryptoSwift.xcframework/tvos-arm64_x86_64-simulator"
		],
		"s": [
			"$(BAZEL_OUT)/tvos-x86_64-min15.0-applebin_tvos-tvos_x86_64-dbg-STABLE-3/bin/Lib"
		]
	},
	"x86_64-apple-tvos-simulator tvOSApp.app/tvOSApp": {
		"c": "-F$(PROJECT_DIR)/external/com_github_krzyzanowskim_cryptoswift/CryptoSwift.xcframework/tvos-arm64_x86_64-simulator -iquote$(PROJECT_DIR)/external/com_github_krzyzanowskim_cryptoswift -iquote$(PROJECT_DIR)/bazel-out/tvos-x86_64-min15.0-applebin_tvos-tvos_x86_64-dbg-STABLE-3/bin/external/com_github_krzyzanowskim_cryptoswift -iquote$(PROJECT_DIR) -iquote$(PROJECT_DIR)/bazel-out/tvos-x86_64-min15.0-applebin_tvos-tvos_x86_64-dbg-STABLE-3/bin -fmodule-map-file=$(PROJECT_DIR)/external/com_github_krzyzanowskim_cryptoswift/CryptoSwift.xcframework/tvos-arm64_x86_64-simulator/CryptoSwift.framework/Modules/module.modulemap -O0 -DDEBUG=1 -fstack-protector -fstack-protector-all -iquote$(PROJECT_DIR)/external/com_github_krzyzanowskim_cryptoswift -iquote$(PROJECT_DIR)/bazel-out/tvos-x86_64-min15.0-applebin_tvos-tvos_x86_64-dbg-STABLE-3/bin/external/com_github_krzyzanowskim_cryptoswift -iquote$(PROJECT_DIR) -iquote$(PROJECT_DIR)/bazel-out/tvos-x86_64-min15.0-applebin_tvos-tvos_x86_64-dbg-STABLE-3/bin -O0 -fstack-protector -fstack-protector-all -iquote$(PROJECT_DIR)/external/com_github_krzyzanowskim_cryptoswift -iquote$(PROJECT_DIR)/bazel-out/tvos-x86_64-min15.0-applebin_tvos-tvos_x86_64-dbg-STABLE-3/bin/external/com_github_krzyzanowskim_cryptoswift -iquote$(PROJECT_DIR) -iquote$(PROJECT_DIR)/bazel-out/tvos-x86_64-min15.0-applebin_tvos-tvos_x86_64-dbg-STABLE-3/bin -O0 -fstack-protector -fstack-protector-all",
		"f": [
			"$(BAZEL_EXTERNAL)/com_github_krzyzanowskim_cryptoswift/CryptoSwift.xcframework/tvos-arm64_x86_64-simulator"
		],
		"s": [
			"$(BAZEL_OUT)/tvos-x86_64-min15.0-applebin_tvos-tvos_x86_64-dbg-STABLE-3/bin/UI",
			"$(BAZEL_OUT)/tvos-x86_64-min15.0-applebin_tvos-tvos_x86_64-dbg-STABLE-3/bin/Lib"
		]
	},
	"x86_64-apple-tvos-simulator tvOSAppUITests.xctest/tvOSAppUITests": {
		"c": "-iquote$(PROJECT_DIR) -iquote$(PROJECT_DIR)/bazel-out/tvos-x86_64-min15.0-applebin_tvos-tvos_x86_64-dbg-STABLE-3/bin -O0 -DDEBUG=1 -fstack-protector -fstack-protector-all"
	},
	"x86_64-apple-tvos-simulator tvOSAppUnitTests.xctest/tvOSAppUnitTests": {
		"c": "-F$(PROJECT_DIR)/external/com_github_krzyzanowskim_cryptoswift/CryptoSwift.xcframework/tvos-arm64_x86_64-simulator -iquote$(PROJECT_DIR)/external/com_github_krzyzanowskim_cryptoswift -iquote$(PROJECT_DIR)/bazel-out/tvos-x86_64-min15.0-applebin_tvos-tvos_x86_64-dbg-STABLE-3/bin/external/com_github_krzyzanowskim_cryptoswift -iquote$(PROJECT_DIR) -iquote$(PROJECT_DIR)/bazel-out/tvos-x86_64-min15.0-applebin_tvos-tvos_x86_64-dbg-STABLE-3/bin -fmodule-map-file=$(PROJECT_DIR)/external/com_github_krzyzanowskim_cryptoswift/CryptoSwift.xcframework/tvos-arm64_x86_64-simulator/CryptoSwift.framework/Modules/module.modulemap -O0 -DDEBUG=1 -fstack-protector -fstack-protector-all -iquote$(PROJECT_DIR)/external/com_github_krzyzanowskim_cryptoswift -iquote$(PROJECT_DIR)/bazel-out/tvos-x86_64-min15.0-applebin_tvos-tvos_x86_64-dbg-STABLE-3/bin/external/com_github_krzyzanowskim_cryptoswift -iquote$(PROJECT_DIR) -iquote$(PROJECT_DIR)/bazel-out/tvos-x86_64-min15.0-applebin_tvos-tvos_x86_64-dbg-STABLE-3/bin -O0 -fstack-protector -fstack-protector-all -iquote$(PROJECT_DIR)/external/com_github_krzyzanowskim_cryptoswift -iquote$(PROJECT_DIR)/bazel-out/tvos-x86_64-min15.0-applebin_tvos-tvos_x86_64-dbg-STABLE-3/bin/external/com_github_krzyzanowskim_cryptoswift -iquote$(PROJECT_DIR) -iquote$(PROJECT_DIR)/bazel-out/tvos-x86_64-min15.0-applebin_tvos-tvos_x86_64-dbg-STABLE-3/bin -O0 -fstack-protector -fstack-protector-all -iquote$(PROJECT_DIR)/external/com_github_krzyzanowskim_cryptoswift -iquote$(PROJECT_DIR)/bazel-out/tvos-x86_64-min15.0-applebin_tvos-tvos_x86_64-dbg-STABLE-3/bin/external/com_github_krzyzanowskim_cryptoswift -iquote$(PROJECT_DIR) -iquote$(PROJECT_DIR)/bazel-out/tvos-x86_64-min15.0-applebin_tvos-tvos_x86_64-dbg-STABLE-3/bin -O0 -fstack-protector -fstack-protector-all",
		"f": [
			"$(BAZEL_EXTERNAL)/com_github_krzyzanowskim_cryptoswift/CryptoSwift.xcframework/tvos-arm64_x86_64-simulator"
		],
		"s": [
			"$(BAZEL_OUT)/tvos-x86_64-min15.0-applebin_tvos-tvos_x86_64-dbg-STABLE-3/bin/tvOSApp/Source",
			"$(BAZEL_OUT)/tvos-x86_64-min15.0-applebin_tvos-tvos_x86_64-dbg-STABLE-3/bin/UI",
			"$(BAZEL_OUT)/tvos-x86_64-min15.0-applebin_tvos-tvos_x86_64-dbg-STABLE-3/bin/Lib"
		]
	},
	"x86_64-apple-watchos-simulator Lib.framework/Lib": {
		"c": "-F$(PROJECT_DIR)/external/com_github_krzyzanowskim_cryptoswift/CryptoSwift.xcframework/watchos-arm64_i386_x86_64-simulator -iquote$(PROJECT_DIR)/external/com_github_krzyzanowskim_cryptoswift -iquote$(PROJECT_DIR)/bazel-out/watchos-x86_64-min7.0-applebin_watchos-watchos_x86_64-dbg-STABLE-2/bin/external/com_github_krzyzanowskim_cryptoswift -iquote$(PROJECT_DIR) -iquote$(PROJECT_DIR)/bazel-out/watchos-x86_64-min7.0-applebin_watchos-watchos_x86_64-dbg-STABLE-2/bin -fmodule-map-file=$(PROJECT_DIR)/external/com_github_krzyzanowskim_cryptoswift/CryptoSwift.xcframework/watchos-arm64_i386_x86_64-simulator/CryptoSwift.framework/Modules/module.modulemap -O0 -DDEBUG=1 -fstack-protector -fstack-protector-all",
		"f": [
			"$(BAZEL_EXTERNAL)/com_github_krzyzanowskim_cryptoswift/CryptoSwift.xcframework/watchos-arm64_i386_x86_64-simulator"
		]
	},
	"x86_64-apple-watchos-simulator LibFramework.watchOS.framework/LibFramework.watchOS": {
		"c": "-F$(PROJECT_DIR)/external/com_github_krzyzanowskim_cryptoswift/CryptoSwift.xcframework/watchos-arm64_i386_x86_64-simulator -iquote$(PROJECT_DIR)/external/com_github_krzyzanowskim_cryptoswift -iquote$(PROJECT_DIR)/bazel-out/watchos-x86_64-min7.0-applebin_watchos-watchos_x86_64-dbg-STABLE-2/bin/external/com_github_krzyzanowskim_cryptoswift -iquote$(PROJECT_DIR) -iquote$(PROJECT_DIR)/bazel-out/watchos-x86_64-min7.0-applebin_watchos-watchos_x86_64-dbg-STABLE-2/bin -fmodule-map-file=$(PROJECT_DIR)/external/com_github_krzyzanowskim_cryptoswift/CryptoSwift.xcframework/watchos-arm64_i386_x86_64-simulator/CryptoSwift.framework/Modules/module.modulemap -O0 -DDEBUG=1 -fstack-protector -fstack-protector-all",
		"f": [
			"$(BAZEL_EXTERNAL)/com_github_krzyzanowskim_cryptoswift/CryptoSwift.xcframework/watchos-arm64_i386_x86_64-simulator"
		]
	},
	"x86_64-apple-watchos-simulator UIFramework.watchOS.framework/UIFramework.watchOS": {
		"c": "-F$(PROJECT_DIR)/external/com_github_krzyzanowskim_cryptoswift/CryptoSwift.xcframework/watchos-arm64_i386_x86_64-simulator -iquote$(PROJECT_DIR)/external/com_github_krzyzanowskim_cryptoswift -iquote$(PROJECT_DIR)/bazel-out/watchos-x86_64-min7.0-applebin_watchos-watchos_x86_64-dbg-STABLE-2/bin/external/com_github_krzyzanowskim_cryptoswift -iquote$(PROJECT_DIR) -iquote$(PROJECT_DIR)/bazel-out/watchos-x86_64-min7.0-applebin_watchos-watchos_x86_64-dbg-STABLE-2/bin -fmodule-map-file=$(PROJECT_DIR)/external/com_github_krzyzanowskim_cryptoswift/CryptoSwift.xcframework/watchos-arm64_i386_x86_64-simulator/CryptoSwift.framework/Modules/module.modulemap -O0 -DDEBUG=1 -fstack-protector -fstack-protector-all -iquote$(PROJECT_DIR)/external/com_github_krzyzanowskim_cryptoswift -iquote$(PROJECT_DIR)/bazel-out/watchos-x86_64-min7.0-applebin_watchos-watchos_x86_64-dbg-STABLE-2/bin/external/com_github_krzyzanowskim_cryptoswift -iquote$(PROJECT_DIR) -iquote$(PROJECT_DIR)/bazel-out/watchos-x86_64-min7.0-applebin_watchos-watchos_x86_64-dbg-STABLE-2/bin -O0 -fstack-protector -fstack-protector-all",
		"f": [
			"$(BAZEL_EXTERNAL)/com_github_krzyzanowskim_cryptoswift/CryptoSwift.xcframework/watchos-arm64_i386_x86_64-simulator"
		],
		"s": [
			"$(BAZEL_OUT)/watchos-x86_64-min7.0-applebin_watchos-watchos_x86_64-dbg-STABLE-2/bin/Lib"
		]
	},
	"x86_64-apple-watchos-simulator watchOSAppExtension.appex/watchOSAppExtension": {
		"c": "-F$(PROJECT_DIR)/external/com_github_krzyzanowskim_cryptoswift/CryptoSwift.xcframework/watchos-arm64_i386_x86_64-simulator -iquote$(PROJECT_DIR)/external/com_github_krzyzanowskim_cryptoswift -iquote$(PROJECT_DIR)/bazel-out/watchos-x86_64-min7.0-applebin_watchos-watchos_x86_64-dbg-STABLE-2/bin/external/com_github_krzyzanowskim_cryptoswift -iquote$(PROJECT_DIR) -iquote$(PROJECT_DIR)/bazel-out/watchos-x86_64-min7.0-applebin_watchos-watchos_x86_64-dbg-STABLE-2/bin -fmodule-map-file=$(PROJECT_DIR)/external/com_github_krzyzanowskim_cryptoswift/CryptoSwift.xcframework/watchos-arm64_i386_x86_64-simulator/CryptoSwift.framework/Modules/module.modulemap -O0 -DDEBUG=1 -fstack-protector -fstack-protector-all -iquote$(PROJECT_DIR)/external/com_github_krzyzanowskim_cryptoswift -iquote$(PROJECT_DIR)/bazel-out/watchos-x86_64-min7.0-applebin_watchos-watchos_x86_64-dbg-STABLE-2/bin/external/com_github_krzyzanowskim_cryptoswift -iquote$(PROJECT_DIR) -iquote$(PROJECT_DIR)/bazel-out/watchos-x86_64-min7.0-applebin_watchos-watchos_x86_64-dbg-STABLE-2/bin -O0 -fstack-protector -fstack-protector-all -iquote$(PROJECT_DIR)/external/com_github_krzyzanowskim_cryptoswift -iquote$(PROJECT_DIR)/bazel-out/watchos-x86_64-min7.0-applebin_watchos-watchos_x86_64-dbg-STABLE-2/bin/external/com_github_krzyzanowskim_cryptoswift -iquote$(PROJECT_DIR) -iquote$(PROJECT_DIR)/bazel-out/watchos-x86_64-min7.0-applebin_watchos-watchos_x86_64-dbg-STABLE-2/bin -O0 -fstack-protector -fstack-protector-all",
		"f": [
			"$(BAZEL_EXTERNAL)/com_github_krzyzanowskim_cryptoswift/CryptoSwift.xcframework/watchos-arm64_i386_x86_64-simulator"
		],
		"s": [
			"$(BAZEL_OUT)/watchos-x86_64-min7.0-applebin_watchos-watchos_x86_64-dbg-STABLE-2/bin/UI",
			"$(BAZEL_OUT)/watchos-x86_64-min7.0-applebin_watchos-watchos_x86_64-dbg-STABLE-2/bin/Lib"
		]
	},
	"x86_64-apple-watchos-simulator watchOSAppExtensionUnitTests.xctest/watchOSAppExtensionUnitTests": {
		"c": "-F$(PROJECT_DIR)/external/com_github_krzyzanowskim_cryptoswift/CryptoSwift.xcframework/watchos-arm64_i386_x86_64-simulator -iquote$(PROJECT_DIR)/external/com_github_krzyzanowskim_cryptoswift -iquote$(PROJECT_DIR)/bazel-out/watchos-x86_64-min7.0-applebin_watchos-watchos_x86_64-dbg-STABLE-2/bin/external/com_github_krzyzanowskim_cryptoswift -iquote$(PROJECT_DIR) -iquote$(PROJECT_DIR)/bazel-out/watchos-x86_64-min7.0-applebin_watchos-watchos_x86_64-dbg-STABLE-2/bin -fmodule-map-file=$(PROJECT_DIR)/external/com_github_krzyzanowskim_cryptoswift/CryptoSwift.xcframework/watchos-arm64_i386_x86_64-simulator/CryptoSwift.framework/Modules/module.modulemap -O0 -DDEBUG=1 -fstack-protector -fstack-protector-all -iquote$(PROJECT_DIR)/external/com_github_krzyzanowskim_cryptoswift -iquote$(PROJECT_DIR)/bazel-out/watchos-x86_64-min7.0-applebin_watchos-watchos_x86_64-dbg-STABLE-2/bin/external/com_github_krzyzanowskim_cryptoswift -iquote$(PROJECT_DIR) -iquote$(PROJECT_DIR)/bazel-out/watchos-x86_64-min7.0-applebin_watchos-watchos_x86_64-dbg-STABLE-2/bin -O0 -fstack-protector -fstack-protector-all -iquote$(PROJECT_DIR)/external/com_github_krzyzanowskim_cryptoswift -iquote$(PROJECT_DIR)/bazel-out/watchos-x86_64-min7.0-applebin_watchos-watchos_x86_64-dbg-STABLE-2/bin/external/com_github_krzyzanowskim_cryptoswift -iquote$(PROJECT_DIR) -iquote$(PROJECT_DIR)/bazel-out/watchos-x86_64-min7.0-applebin_watchos-watchos_x86_64-dbg-STABLE-2/bin -O0 -fstack-protector -fstack-protector-all",
		"f": [
			"$(BAZEL_EXTERNAL)/com_github_krzyzanowskim_cryptoswift/CryptoSwift.xcframework/watchos-arm64_i386_x86_64-simulator"
		],
		"s": [
			"$(BAZEL_OUT)/watchos-x86_64-min7.0-applebin_watchos-watchos_x86_64-dbg-STABLE-2/bin/UI",
			"$(BAZEL_OUT)/watchos-x86_64-min7.0-applebin_watchos-watchos_x86_64-dbg-STABLE-2/bin/Lib"
		]
	},
	"x86_64-apple-watchos-simulator watchOSAppUITests.xctest/watchOSAppUITests": {
		"c": "-iquote$(PROJECT_DIR) -iquote$(PROJECT_DIR)/bazel-out/watchos-x86_64-min7.0-applebin_watchos-watchos_x86_64-dbg-STABLE-2/bin -O0 -DDEBUG=1 -fstack-protector -fstack-protector-all"
	}
}

def __lldb_init_module(debugger, _internal_dict):
    # Register the stop hook when this module is loaded in lldb
    ci = debugger.GetCommandInterpreter()
    res = lldb.SBCommandReturnObject()
    ci.HandleCommand(
        "target stop-hook add -P swift_debug_settings.StopHook",
        res,
    )
    if not res.Succeeded():
        print(f"""\
Failed to register Swift debug options stop hook:

{res.GetError()}
Please file a bug report here: \
https://github.com/MobileNativeFoundation/rules_xcodeproj/issues/new?template=bug.md
""")
        return

def _get_relative_executable_path(module):
    for extension in _BUNDLE_EXTENSIONS:
        prefix, _, suffix = module.rpartition(extension)
        if prefix:
            return prefix.split("/")[-1] + extension + suffix
    return module.split("/")[-1]

class StopHook:
    "An lldb stop hook class, that sets swift settings for the current module."

    def __init__(self, _target, _extra_args, _internal_dict):
        pass

    def handle_stop(self, exe_ctx, _stream):
        "Method that is called when the user stops in lldb."
        module = exe_ctx.frame.module
        if not module:
            return

        module_name = module.file.__get_fullpath__()
        versionless_triple = _TRIPLE_MATCH.sub(r"\1\2\3", module.GetTriple())
        executable_path = _get_relative_executable_path(module_name)
        key = f"{versionless_triple} {executable_path}"

        settings = _SETTINGS.get(key)

        if settings:
            frameworks = " ".join([
                f'"{path}"'
                for path in settings.get("f", [])
            ])
            if frameworks:
                lldb.debugger.HandleCommand(
                    f"settings set -- target.swift-framework-search-paths {frameworks}",
                )
            else:
                lldb.debugger.HandleCommand(
                    "settings clear target.swift-framework-search-paths",
                )

            includes = " ".join([
                f'"{path}"'
                for path in settings.get("s", [])
            ])
            if includes:
                lldb.debugger.HandleCommand(
                    f"settings set -- target.swift-module-search-paths {includes}",
                )
            else:
                lldb.debugger.HandleCommand(
                    "settings clear target.swift-module-search-paths",
                )

            clang = settings.get("c")
            if clang:
                lldb.debugger.HandleCommand(
                    f"settings set -- target.swift-extra-clang-flags '{clang}'",
                )
            else:
                lldb.debugger.HandleCommand(
                    "settings clear target.swift-extra-clang-flags",
                )

        return True
