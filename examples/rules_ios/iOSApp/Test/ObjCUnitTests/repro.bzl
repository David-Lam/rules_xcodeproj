load(
    "@build_bazel_rules_ios//rules:test.bzl",
    rules_ios_ios_unit_test = "ios_unit_test",
)

def macro(name):
    rules_ios_ios_unit_test(
        name = "iOSAppObjCUnitTests",
        srcs = native.glob(["**/*.m"]),
        bundle_id = "rules-xcodeproj.example.objctests",
        bundle_name = "iOS_App_ObjC_UnitTests",
        minimum_os_version = "15.0",
        module_name = "iOSAppObjCUnitTests",
        tags = ["manual"],
        test_host = "//iOSApp",
        visibility = ["@rules_xcodeproj//xcodeproj:generated"],
        deps = [
            "//iOSApp/Source:iOSApp.library",
            "//iOSApp/Source/Utils",
        ],
    )

    rules_ios_ios_unit_test(
        name = "iOSAppObjCUnitTestSuite",
        srcs = native.glob(["**/*.m"]),
        bundle_id = "rules-xcodeproj.example.objctests",
        minimum_os_version = "15.0",
        module_name = "iOSAppObjCUnitTestSuite",
        runners = [
            ":iPhone-13-Pro__16.2",
            ":iPad-Air-4th-gen__16.2",
        ],
        tags = ["manual"],
        test_host = "//iOSApp",
        visibility = ["@rules_xcodeproj//xcodeproj:generated"],
        deps = [
            "//iOSApp/Source:iOSApp.library",
            "//iOSApp/Source/Utils",
        ],
    )
