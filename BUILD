load("@rules_python//python:defs.bzl", "py_binary")
load("@scraper_deps//:requirements.bzl", "requirement")

py_binary(
    name = "mr_lodge",
    srcs = ["scrapper.py"],
    args = ["--mr_lodge"],
    main = "scrapper.py",
    deps = [
        "//mr_lodge:mr_lodge_scrapper",
        requirement("pandas"),
    ],
)

py_binary(
    name = "cognomix",
    srcs = ["scrapper.py"],
    args = ["--cognomix"],
    main = "scrapper.py",
    deps = [
        "//cognomix:cognomix_scrapper",
        requirement("pandas"),
    ],
)

py_binary(
    name = "currencies_rates",
    srcs = ["scrapper.py"],
    args = ["--currencies_rates"],
    main = "scrapper.py",
    deps = [
        "//currencies_rates:currency_rates_scrapper",
        requirement("pandas"),
    ],
)
