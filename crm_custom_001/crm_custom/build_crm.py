import os
import shutil
import subprocess
from pathlib import Path


BENCH = Path(__file__).resolve().parents[4]

CRM_FRONTEND = BENCH / "apps" / "crm" / "frontend"

CUSTOM_FRONTEND = (
    BENCH
    / "apps"
    / "crm_custom_001"
    / "crm_custom_001"
    / "crm_custom"
    / "frontend"
)

BUILD_DIR = CUSTOM_FRONTEND / ".crm_build"


def copy_source():
    if BUILD_DIR.exists():
        shutil.rmtree(BUILD_DIR)

    shutil.copytree(
        CRM_FRONTEND,
        BUILD_DIR,
        ignore=shutil.ignore_patterns(
            "node_modules",
            "dist",
            ".vite",
        ),
    )


def apply_overrides():
    custom_src = CUSTOM_FRONTEND / "src"

    override_router = (
        CUSTOM_FRONTEND
        / "src_override"
        / "router.js"
    )

    override_sidebar = (
        CUSTOM_FRONTEND
        / "src_override"
        / "components"
        / "Layouts"
        / "AppSidebar.vue"
    )

    custom_pages = CUSTOM_FRONTEND / "src" / "pages"

    build_src = BUILD_DIR / "src"

    # router override
    shutil.copy2(
        override_router,
        build_src / "router.js",
    )

    # sidebar override
    sidebar_target = (
        build_src
        / "components"
        / "Layouts"
        / "AppSidebar.vue"
    )

    sidebar_target.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    shutil.copy2(
        override_sidebar,
        sidebar_target,
    )

    # custom pages
    for page in custom_pages.glob("*.vue"):
        shutil.copy2(
            page,
            build_src / "pages" / page.name,
        )


def build():
    env = os.environ.copy()

    subprocess.run(
        ["yarn", "build"],
        cwd=BUILD_DIR,
        env=env,
        check=True,
    )


def copy_build():
    source = BUILD_DIR / "dist"

    target = (
        BENCH
        / "apps"
        / "crm"
        / "crm"
        / "public"
        / "frontend"
    )

    if not source.exists():
        raise RuntimeError(
            f"Build output not found: {source}"
        )

    if target.exists():
        shutil.rmtree(target)

    shutil.copytree(
        source,
        target,
    )

    print("CRM custom frontend copied successfully.")


def main():
    print("1. Copying CRM frontend...")
    copy_source()

    print("2. Applying custom overrides...")
    apply_overrides()

    print("3. Building CRM frontend...")
    build()

    print("4. Copying build output...")
    copy_build()

    print("DONE")


if __name__ == "__main__":
    main()
