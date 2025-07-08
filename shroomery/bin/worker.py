from structlog import get_logger

def main():
  logger = get_logger()

  logger.info("starting worker")

if __name__ == "__main__":
  main()