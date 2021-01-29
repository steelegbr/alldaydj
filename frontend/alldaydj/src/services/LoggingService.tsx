import log from "loglevel";

export const getLogger = () => {
    const logger = log.getLogger("alldaydj");
    logger.enableAll();
    return logger;
};
