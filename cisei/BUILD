load("@rules_python//python:defs.bzl", "py_library")
load("@io_bazel_rules_docker//python3:image.bzl", "py3_image")
load("@io_bazel_rules_docker//container:container.bzl", "container_image", "container_push")
load("@scraper_deps//:requirements.bzl", "requirement")

package(default_visibility = ["//visibility:public"])

py_library(
    name = "cisei_scrapper",
    srcs = [
        "cisei_scrapper.py",
        "names.py",
    ],
    data = [
        "//cognomix:names",
    ],
    deps = [
        requirement("tenacity"),
        requirement("psycopg2-binary"),
        requirement("pydantic"),
    ],
)

container_image(
    name = "ubuntu_python3",
    base = "@ubuntu_python3//image",
)

py3_image(
    name = "cisei_image",
    srcs = ["cisei_runner.py"],
    base = "ubuntu_python3",
    main = "cisei_runner.py",
    deps = [":cisei_scrapper"],
)

container_push(
    name = "push_cisei_image",
    format = "Docker",
    image = "cisei_image",
    registry = "index.docker.io",
    repository = "framaxwlad/cisei",
    tag = "$(image_tag)",
    tags = ["manual"],
)
