import log, { Logger } from 'loglevel'

export const getLogger = (): Logger => {
  const logger = log.getLogger('alldaydj')
  logger.enableAll()
  return logger
}
