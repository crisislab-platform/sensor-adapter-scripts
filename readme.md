# Sensor adapter scripts

This repo has a collection of scripts to adapt the output of different ground motion sensors to a format our server understands (the Raspberry Shake format).

If you're using a Raspberry Shake device, you probably don't need these details.

Also check out the [How to set up a sensor](https://docs.google.com/document/d/1l8SA2pNLpueWjAy0l3gStlXXv-Tw3wwl3vfgqVdrA8s/edit?usp=sharing) document, which goes over setting up the networking parts.

## Usage

1. Select the correct script for your device.
2. Set up a Raspberry PI (or other device) connected to the device directly, either via ethernet or usb (USB is currently is only for the CRISiSlab/Mithira sensor).
3. Do the networking setup as described in [How to set up a sensor](https://docs.google.com/document/d/1l8SA2pNLpueWjAy0l3gStlXXv-Tw3wwl3vfgqVdrA8s/edit?usp=sharing).
4. Follow the instructions in the relevant readme.md file to set up the adapter script for that device.
5. Update the server IP if not using our main server hosted on Massey infra.

## Adding a new adapter

1. Review existing adapters.
2. Copy paste the one that looks closest to what you'll be doing.
3. Replace the parts that read data from the sensor to work with your sensor.
4. Test with first a local version of the [ingest server](https://github.com/crisislab-platform/ingest-deno) and then the live version.
5. Update the instructions if needed.
6. Commit to the repo.

### More details

Fundamentally, the hard part is getting data out of a sensor. Once you have it (and have internet access) you just need to arrange it in the following format, encode it as `utf-8` binary, then send it to `10.241.144.172:2098` over UDP.

```
{'channel', timestamp (in seconds not ms), num1, num2, num3, ..., num250}
```

E.g.

```
{'HNZ', 1722946951.674587, 1,2,3,4,5,6,7,8}
```

This is based on the Raspberry Shake data format. Thinks to remember:

- The channel should be 3 upper-case letters
- The timestamp is **in seconds not milliseconds**
- Spaces are optional
- You can have any number of readings, but around 250 is normal
