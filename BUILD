load("@rules_python//python:defs.bzl", "py_binary")

py_binary(
    name = "mr_lodge",
    main = "scrapper.py",
    srcs = ["scrapper.py"],
    args = ["--mr_lodge"],
    deps = ["//mr_lodge:mr_lodge_scrapper"],
)
