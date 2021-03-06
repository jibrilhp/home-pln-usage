## About The Project

I'm using a PLN prepaid meter. On a prepaid meter, I can see the stats about measurement KWH, ampere, voltage, time, and the most important things my credit. Unfortunately, I don't know the stats can be saved to my database or I can see them on the PLN website. To solve this problem I create python code to read the impulse lamp on the prepaid meter and count it. Hopefully this useful for you :)

## Getting Started

you can use the virtual environment or global settings, I'm using python 3.7 to run this code.

### Prerequisites Library

```sh
pip install pandas
pip install SQLAlchemy
```

### Prerequisites Hardware

you may need another camera to capture the impulse lamp a prepaid meter

## Preparation

    1. Install PostgreSQL on your computer
    2. Set username postgres, password 12345678 or other configuration (you can change on conn variable too)
    3. Create a database named plnstats

## Execute

    1. Run the kwh_pln_sensor.py to read continuously impulse lamp on a prepaid meter
    2. Run the kwh_pln_usage.py to summarise yesterday usage.

<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

    1. Fork the Project
    2. Create your Feature Branch (`git checkout -b something/SomethingFeature`)
    3. Commit your Changes (`git commit -m 'Add some SomethingFeature'`)
    4. Push to the Branch (`git push origin feature/SomethingFeature`)
    5. Open a Pull Request



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.


