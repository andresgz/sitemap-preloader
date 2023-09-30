# Website SiteMap Preloader

Package for preloading website URLS from a provided SITEMAP URL.
You can use this package to preload your website URLS in the background, so that your website will be faster for your users.
You can set the depth in case It has more than one level.

## Requirements
* Python 3.6+

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install preloader.

```
    pip install .
```

## How to use

Follow the steps below to use the package on a python project.

```
    from preloader import Preloader
    sitemap_url = 'https://www.example.com/sitemap.xml'
    preloader = Preloader(sitemap_url, depth=2)
```

## Testing
We use pytest for testing. To run the tests, run the following command in the root directory of the project.
    
```
    pytest
    
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
