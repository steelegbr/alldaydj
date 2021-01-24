import log from 'loglevel';

export const getLogger = () => {
    let logger = log.getLogger("alldaydj");
    logger.enableAll();
    return logger;
}