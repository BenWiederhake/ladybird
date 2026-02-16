#!/usr/bin/env python3

import subprocess


TEST_FILENAME = "Tests/LibWeb/Text/input/named-node-map-supported-property-names-accidentally-quadratic.html"
TEST_PREAMBLE = """
<!DOCTYPE html>
<script src="include.js"></script>
<span id="manyattr"
"""
TEST_EPILOGUE = """
>
</span>
<script>
    test(() => {
        var element_with_many_attributes = document.getElementById("manyattr");
        var begin = performance.now();
        Object.getOwnPropertyNames(element_with_many_attributes.attributes); // too many calls, additional problem above in call stack
        //Object.getOwnPropertySymbols(element_with_many_attributes.attributes); // again
        //Object.getOwnPropertyDescriptors(element_with_many_attributes.attributes); // Even slower!
        //Reflect.ownKeys(element_with_many_attributes.attributes);
        //Object.keys(element_with_many_attributes.attributes);
        //Object.hasOwn(element_with_many_attributes.attributes, "foobar");
        var end = performance.now();
        println(`${end - begin}`);
    });
</script>
"""


def alpha(integer):
    numeric_str = f"{integer:09}"
    alpha_str = numeric_str \
        .replace("0", "a") \
        .replace("1", "b") \
        .replace("2", "c") \
        .replace("3", "d") \
        .replace("4", "e") \
        .replace("5", "f") \
        .replace("6", "g") \
        .replace("7", "h") \
        .replace("8", "i") \
        .replace("9", "j")
    return alpha_str


def single_measurement(num_attrs):
    with open(TEST_FILENAME, "w") as fp:
        fp.write(TEST_PREAMBLE)
        fp.write("".join(f" foo{alpha(i)}=\"1234\"" for i in range(num_attrs)))
        fp.write(TEST_EPILOGUE)
    result = subprocess.run(
        [
            "./Meta/ladybird.py",
            "run",
            "ladybird",
            "--headless=text",
            "--test-mode",
            TEST_FILENAME,
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    duration_ms = result.stdout.split("\n")[3]
    print(f"{num_attrs},{duration_ms}", flush=True)


RANGE_START = 60
RANGE_END = 2000
RANGE_STEPS = 50
RANGE_FACTOR = RANGE_END / RANGE_START


def run():
    for i in range(RANGE_STEPS):
        i_frac = i / (RANGE_STEPS - 1)
        num_attrs = round(RANGE_START * RANGE_FACTOR ** i_frac)
        single_measurement(num_attrs)


if __name__ == "__main__":
    run()
