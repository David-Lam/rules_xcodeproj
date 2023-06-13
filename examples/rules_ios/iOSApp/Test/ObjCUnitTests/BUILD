load(
    "@build_bazel_rules_apple//apple/testing/default_runner:ios_test_runner.bzl",
    "ios_test_runner",
)
load(
    "//iOSApp/Test/ObjCUnitTests:repro.bzl",
    "macro",
)

ios_test_runner(
    name = "iPhone-13-Pro__16.2",
    device_type = "iPhone 13 Pro",
    os_version = "16.2",
)

ios_test_runner(
    name = "iPad-Air-4th-gen__16.2",
    device_type = "iPad Air (4th generation)",
    os_version = "16.2",
)

macro(name = "repro")
