load("@rules_python//python:defs.bzl", "py_library")
load("@scraper_deps//:requirements.bzl", "requirement")

package(default_visibility = ["//visibility:public"])

py_library(
    name = "cisei_scrapper",
    srcs = glob(["*.py"]),
    data = [
        "//cognomix:names",
    ],
    deps = [
        requirement("tenacity"),
        requirement("pydantic"),
    ],
)
