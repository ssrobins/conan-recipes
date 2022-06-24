#!/usr/bin/env python3

# TODO: Add check to make sure there are no non-hidden files in recipe dir

import os.path
import subprocess


def get_recipe_name(recipe_string):
    recipe_name = str()
    recipe_name = recipe_string.split("/")[0]
    recipe_name = recipe_name.replace("conanfile.py (", "")
    return recipe_name


def main():
    recipe_root_path = f"{os.path.dirname(os.path.realpath(__file__))}/../recipes"

    recipe_names = sorted(f for f in os.listdir(recipe_root_path) if not f.startswith("."))
    print(recipe_names)

    for recipe in recipe_names:
        recipe_path = os.path.join(recipe_root_path, recipe)
        conan_info = f"conan info . --only None"
        print(conan_info, flush=True)
        conan_info_output = subprocess.run(conan_info, cwd=recipe_path, shell=True, check=True, stdout=subprocess.PIPE)
        print(conan_info_output)


# conan export ../recipes/ssrobins_engine ssrobins_engine/1.2.0
# conan lock create --build --reference=ssrobins_engine/1.2.0 --lockfile-out=ssrobins_engine.lock
# conan lock build-order ssrobins_engine.lock --json=ssrobins_engine_build_order.json


if __name__ == "__main__":
    main()
