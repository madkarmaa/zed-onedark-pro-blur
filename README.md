# OneDark Pro Blur

[![Sync themes](https://github.com/madkarmaa/zed-onedark-pro-blur/actions/workflows/sync.yml/badge.svg)](https://github.com/madkarmaa/zed-onedark-pro-blur/actions/workflows/sync.yml)

A [Zed](https://zed.dev) theme extension that ports **[Binaryify/OneDark-Pro](https://github.com/Binaryify/OneDark-Pro)** and adds translucent, blurred backgrounds to every variant.

### Installing from source (dev extension)

```sh
git clone https://github.com/madkarmaa/zed-onedark-pro-blur
```

Then in Zed: command palette -> `zed: install dev extension` -> select the cloned folder.

## Local development

**Prerequisites**: `git`, the [Rust toolchain](https://rustup.rs), and [`uv`](https://docs.astral.sh/uv/getting-started/installation/).

Unix:
```sh
./sync.sh
```

Windows:
```batch
.\sync.bat
```

## Credits

- [Binaryify/OneDark-Pro](https://github.com/Binaryify/OneDark-Pro) - original theme and color values.
- [zed-industries/zed](https://github.com/zed-industries/zed) - the editor and the `theme_importer` tool used for VS Code -> Zed theme conversion.

## Contributing

Contributions are welcome! Feel free to [open an issue](https://github.com/madkarmaa/zed-onedark-pro-blur/issues/new) or submit a pull request if you'd like to fix any bugs.

## License

This project is licensed under the [MIT License](./LICENSE).
