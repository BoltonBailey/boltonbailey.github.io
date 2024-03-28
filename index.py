from htmldoom import base as b
from htmldoom import elements as e
from htmldoom import render as _render
from htmldoom import renders

doctype = _render(b.doctype("html"))

contents = _render(
    e.div(
        class_="mx-auto px-2 min-h-screen min-h-full w-full md:w-3/4 lg:w-1/2 xl:w-1/2 bg-white shadow-md"
    )(
        e.div(class_="flex purple text-xl")(
            e.div(
                class_="w-64 h-auto border-b-2 border-black pt-8 px-2  font-bold"
            )(" Welcome to my website ")
        ),
        e.div(class_="flex purple")(
            e.div(class_="flex-no-shrink w-4 h-auto border-r-2 border-black"),
            e.div(
                class_="w-auto h-auto border-l-8 border-purple-lighter pl-3 py-1 "
            )(
                e.p(class_="border-l-4 border-purple-light pl-2 my-2")(
                    " Hi! "
                ),
                e.img(
                    src="boltonbailey.JPG",
                    alt="Imagine a picture of me",
                    width="250",
                    height="300",
                    float_="left",
                ),
                e.p(class_="border-l-4 border-purple-light pl-2 my-2")(
                    "My name is ",
                    e.a(href="mailto:boltonb2@illinois.edu")("Bolton Bailey"),
                    ".",
                ),
                e.p(class_="border-l-4 border-purple-light pl-2 my-2")(
                    "I am a second.5-year Ph.D. student at ",
                    e.a(href="https://cs.illinois.edu/")("UIUC"),
                    ", where I am advised by the venerable ",
                    e.a(href="http://mjt.web.engr.illinois.edu/")(
                        "Matus Telgarsky"
                    ),
                    " (from whom I stole this website layout).",
                ),
                e.p(class_="border-l-4 border-purple-light pl-2 my-2")(
                    "I prove things about neural networks."
                ),
            ),
        ),
        e.div(class_="flex blue text-xl")(
            e.div(
                class_="w-64 h-auto border-b-2 border-black pt-8 px-2  font-bold"
            )(" Research: ")
        ),
        e.div(class_="flex blue")(
            e.div(class_="flex-no-shrink w-4 h-auto border-r-2 border-black"),
            e.div(
                class_="w-auto h-auto border-l-8 border-indigo-lighter pl-3 py-1 "
            )(
                e.p(class_="border-l-4 border-indigo-light pl-2 my-2")(
                    " During summer of 2019, I am visiting the ",
                    e.strong()(
                        e.a(
                            href="https://simons.berkeley.edu/programs/dl2019"
                        )("Simons Institute")
                    ),
                    ". ",
                ),
                e.p(class_="border-l-4 border-indigo-light pl-2 my-2")(
                    " In 2019, I received a ",
                    e.strong()("NSF Graduate Research Fellowship"),
                    ". ",
                ),
                e.p(class_="border-l-4 border-indigo-light pl-2 my-2")(
                    e.strong()(
                        "A Gradual, Semi-Discrete Approach to Generative Network Training via Explicit Wasserstein Minimization"
                    ),
                    " (With Yucheng Chen, Matus Telgarsky, Chao Zhang, Daniel Hsu, Jian Peng) ",
                    e.a(href="http://proceedings.mlr.press/v97/chen19h.html")(
                        "ICML 2019"
                    ),
                    ". (",
                    e.a(href="https://arxiv.org/abs/1906.03471")("arxiv"),
                    ") ",
                ),
                e.p(class_="border-l-4 border-indigo-light pl-2 my-2")(
                    e.strong()("Size-Noise Tradeoffs in Generative Networks"),
                    " (With Matus Telgarsky) ",
                    e.a(
                        href="https://nips.cc/Conferences/2018/Schedule?showEvent=12564"
                    )("NeurIPS 2018 Spotlight"),
                    ". (",
                    e.a(href="https://arxiv.org/abs/1810.11158")("arxiv"),
                    ") (",
                    e.a(
                        href="https://neurips.cc/media/Slides/nips/2018/220cd(04-10-05)-04-10-25-12564-Size-Noise_Trad.pdf"
                    )("slides"),
                    ") (",
                    e.a(
                        href="https://www.videoken.com/embed/1FsBeeO_5hY?tocitem=19"
                    )("video"),
                    ") ",
                ),
                e.p(class_="border-l-4 border-indigo-light pl-2 my-2")(
                    e.strong()("Other interests:")
                ),
                e.p(class_="border-l-4 border-indigo-light pl-2 my-2")(
                    " The power of shallow networks "
                ),
                e.p(class_="border-l-4 border-indigo-light pl-2 my-2")(
                    " Adversarial attacks on neural networks "
                ),
                e.p(class_="border-l-4 border-indigo-light pl-2 my-2")(
                    " Deep RL "
                ),
            ),
        ),
        e.div(class_="flex red text-xl")(
            e.div(
                class_="w-64 h-auto border-b-2 border-black pt-8 px-2  font-bold"
            )(" Teaching Assistantships: ")
        ),
        e.div(class_="flex red")(
            e.div(class_="flex-no-shrink w-4 h-auto border-r-2 border-black"),
            e.div(
                class_="w-auto h-auto border-l-8 border-red-lighter pl-3 py-1 "
            )(
                e.p(class_="border-l-4 border-red-light pl-2 my-2")(
                    e.span(class_="font-bold ")(
                        e.a(
                            href="https://courses.engr.illinois.edu/ece543/sp2019/"
                        )("Statistical Learning Theory (ECE 543)"),
                        ":",
                    ),
                    " spring 2019 ",
                ),
                e.p(class_="border-l-4 border-red-light pl-2 my-2")(
                    e.span(class_="font-bold ")(
                        e.a(
                            href="https://caltech.typepad.com/caltech_as_it_happens/2017/04/cooking-class.html"
                        )("Cooking Basics (at Caltech)"),
                        ":",
                    ),
                    " 2016-2017 ",
                ),
            ),
        ),
        e.br(),
        e.div()("Last updated June 2019"),
    )
)


@renders(e.title()("Bolton Bailey"))
def render_title(data):
    return {}


@renders(
    e.head()(
        e.meta(charset="utf-8"),
        e.meta(name="viewport", content="width=device-width, initial-scale=1"),
        "{title}",
        e.link(
            href="https://cdn.jsdelivr.net/npm/tailwindcss/dist/tailwind.min.css",
            rel="stylesheet",
        ),
        e.style(type_="text/css")(
            b'\n    /* body {{\n    <link href="https://fonts.googleapis.com/css?family=Rokkitt" rel="stylesheet">\n            font-family: \'Rokkitt\', serif;\n              font-size: 150%;\n      }} */\n\n    .purple {{\n      color: rgb(124, 25, 124);\n    }}\n\n    .purple a:hover {{\n      color: rgb(124, 25, 124);\n      background-color: rgb(203, 153, 203);\n    }}\n\n    .purple a:visited {{\n      color: rgb(70, 29, 70);\n    }}\n\n    .purple a {{\n      color: rgb(203, 153, 203);\n    }}\n\n    .blue {{\n      color: rgb(22, 56, 101);\n    }}\n\n    .blue a:hover {{\n      color: rgb(22, 56, 101);\n      background-color: rgb(108, 149, 203);\n    }}\n\n    .blue a:visited {{\n      color: rgb(30, 39, 52);\n    }}\n\n    .blue a {{\n      color: rgb(62, 96, 141);\n    }}\n\n    .red {{\n      color: rgb(100, 31, 34);\n    }}\n\n    .red a:hover {{\n      color: rgb(100, 31, 34);\n      background-color: rgb(151, 85, 87);\n    }}\n\n    .red a:visited {{\n      color: rgb(60, 22, 23);\n    }}\n\n    .red a {{\n      color: rgb(191, 71, 75);\n    }}\n\n    .orange {{\n      color: rgb(147, 94, 15);\n    }}\n\n    .orange a:hover {{\n      color: rgb(147, 94, 15);\n      background-color: rgb(213, 171, 108);\n    }}\n\n    .orange a:visited {{\n      color: rgb(94, 69, 30);\n    }}\n\n    .orange a {{\n      color: rgb(208, 147, 57);\n    }}\n  '
        ),
    )
)
def render_head(data, title_renderer=render_title):
    return {"title": title_renderer(data=data)}


@renders(e.body()("{contents}"))
def render_body(data) -> None:
    return {"contents": contents}


@renders(
    e.html()(
        "{head}",
        b.comment('<body class="font-serif">'),
        b.comment('<body class="bg-yellow-lighter">'),
        "{body}",
    )
)
def render_html(
    data,
    title_renderer=render_title,
    head_renderer=render_head,
    body_renderer=render_body,
):
    return {
        "head": head_renderer(data=data, title_renderer=render_title),
        "body": body_renderer(data=data),
    }


@renders("{doctype}{html}")
def render_document(
    data,
    title_renderer=render_title,
    head_renderer=render_head,
    body_renderer=render_body,
    html_renderer=render_html,
):
    return {
        "doctype": doctype,
        "html": html_renderer(
            data=data,
            title_renderer=title_renderer,
            head_renderer=head_renderer,
            body_renderer=body_renderer,
        ),
    }


def render(data):
    return render_document(data=data)


if __name__ == "__main__":
    print(render({}))

