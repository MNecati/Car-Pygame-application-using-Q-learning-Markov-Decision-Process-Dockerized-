# Car-Pygame-application-using-Q-learning-Markov-Decision-Process-Dockerized-

# Application Usage

Below you'll find instructions on how to use the application with two different methods:

## 1. Using Docker

### Prerequisites:

- Ensure you have **VcXsrv** installed on your Windows machine.
  
  - [Download VcXsrv for Windows](https://sourceforge.net/projects/vcxsrv/)
  
  - After downloading, run the VcXsrv to set it up.

### Steps:

1. Pull the docker image from the repository:
   
 ```bash
   docker pull mnecati/markovneco:v1
```

2. Run the docker container:

 ```bash
   docker run -it --rm -e DISPLAY=host.docker.internal:0.0 mnecati/markovneco:v1
```

## 2. Running without Docker

### Steps:

1. Download the `MDP neco.py` file and the `images` folder from GitHub.

2. After downloading, you need to comment out the Docker-specific path in the code, which is on line 13.

 ```bash
   # image_path = "/usr/src/app/images/" (put # at the start)
```

3. Activate the path in line 10 and provide the correct path:

  ```bash
   image_path = "C:/Users/pc/desktop/your_example_file/images/" (remove # at the start)
  ```
