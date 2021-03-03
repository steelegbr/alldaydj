/* eslint-disable import/prefer-default-export */
import log, { Logger } from 'loglevel';

export const getLogger = (): Logger => {
  const logger = log.getLogger('alldaydj');
  logger.enableAll();
  return logger;
};
