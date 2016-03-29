import setuptools


if __name__ == '__main__':
    setuptools.setup(
        name="shoop-mailchimp",
        version="0.3.1",
        description="Shoop Mailchimp Integration",
        packages=setuptools.find_packages(),
        install_requires=["mailchimp3"],
        include_package_data=True,
        entry_points={"shoop.addon": "shoop_mailchimp=shoop_mailchimp"}
    )
