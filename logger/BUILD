load("@rules_python//python:defs.bzl", "py_library")
load("@scraper_deps//:requirements.bzl", "requirement")

package(default_visibility = ["//visibility:public"])

py_library(
    name = "cisei_logger",
    srcs = glob(["*.py"]),
    deps = [
        requirement("psycopg2-binary"),
    ],
)
