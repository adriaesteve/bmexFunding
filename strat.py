from datetime import datetime
from dateutil import tz
import signal
import schedule
import threading
from time import sleep

from market_maker.utils import log

from bot import FundingBot
import settings


logger = log.setup_custom_logger('strat')


def half_funding(bot: FundingBot) -> None:
    """4 hours until funding: enter a position
    if funding is negative, go long
    if funding is positive, go short
    """

    logger.info('INICI half_funding')

    bot.could_hedge = False

    bot.exit_position(market=False, wait_for_fill=False)

    bot.cancel_open_orders()

    funding_rate = bot.get_funding_rate()

    logger.info('funding rate: %.4f%%' % (funding_rate * 100))

    if funding_rate < 0:
        side = 'Buy'
        quantity = settings.POSITION_SIZE_BUY
    else:
        side = 'Sell'
        quantity = settings.POSITION_SIZE_SELL
    
    sortida = bot.enter_position(side, quantity, market=False)
    logger.info('Sortida enter_position: %s' % str(sortida))
    
    logger.info('FI half_funding')

def funding_over(bot: FundingBot) -> None:
    """funding is over, exit all positions"""

    logger.info('INICI funding_over')
    
    sleep(15)
    
    bot.exit_position(market=False, wait_for_fill=False)
    
    logger.info('FI funding_over')


def main() -> None:
    """place bitmex orders based on current funding rate

    if 4 hours until funding: enter a position
    if funding is negative, go long
    if funding is positive, go short
    if the price moves negatively 1.5% away from a position, exit the position
    if funding is over, exit all positions
    """

    bot = FundingBot()

    signal.signal(signal.SIGTERM, bot.exit)
    signal.signal(signal.SIGINT, bot.exit)
    
    #Test
    #bot.print_status()
    #half_funding(bot)
    #Fi test
    
    schedule.every().day.at(settings.HF_A).do(half_funding, bot)
    schedule.every().day.at(settings.FO_A).do(funding_over, bot)
    schedule.every().day.at(settings.HF_B).do(half_funding, bot)
    schedule.every().day.at(settings.FO_B).do(funding_over, bot)
    schedule.every().day.at(settings.HF_C).do(half_funding, bot)
    schedule.every().day.at(settings.FO_C).do(funding_over, bot)

    def run_scheduled() -> None:
        while True:
            schedule.run_pending()
            sleep(1)
    
    sched = threading.Thread(target=run_scheduled)
    sched.daemon = True
    sched.start()
    
    try:
        bot.run_loop()
    except Exception as e:
        logger.error('bot exiting with exception: %s' % str(e))

        bot.exit()


if __name__ == '__main__':
    main()
