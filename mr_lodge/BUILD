load("@rules_python//python:defs.bzl", "py_library")
load("@scraper_deps//:requirements.bzl", "requirement")

package(default_visibility = ["//visibility:public"])

py_library(
    name = "mr_lodge_scrapper",
    srcs = glob(["*.py"]),
    deps = [
        requirement("pandas"),
    ],
)
