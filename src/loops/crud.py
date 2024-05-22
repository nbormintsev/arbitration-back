from src.database import database_manager


async def get_loops() -> str:
    pool = await database_manager.get_pool()

    return await pool.fetchval(
        """
        select
            json_agg(
                json_build_object(
                    'id', ld.loop_id,
                    'rate_100_percent', ld.rate100_percent,
                    'rate_1000_percent', ld.rate1000_percent,
                    'rate_10000_percent', ld.rate10000_percent,
                    'avg_rate100_percent', ld.avg_rate100_percent,
                    'avg_rate1000_percent', ld.avg_rate1000_percent,
                    'avg_rate10000_percent', ld.avg_rate10000_percent,
                    'courses', ld.course_details,
                    'deal_cnt', ld.deal_cnt,
                    'last_update', ld.last_update,
                    'creation_time', ld.creation_time
                )
            )
        from (
            select
                l.id as loop_id,
                l.rate100_percent,
                l.rate1000_percent,
                l.rate10000_percent,
                l.avg_rate100_percent,
                l.avg_rate1000_percent,
                l.avg_rate10000_percent,
                l.courses,
                l.deal_cnt,
                l.last_update,
                l.creation_time,
                json_agg(
                    json_build_object(
                        'id', c.id,
                        'platform_from', pf.name,
                        'platform_to', pt.name,
                        'currency_from', cf.name,
                        'currency_to', ct.name,
                        'best_price', c.best_price,
                        'liquidity_rates', c.liquidity_rates,
                        'is_open', c.is_open,
                        'last_update', c.last_update
                    )
                ) as course_details
            from
                loops l
            join
                courses c on c.id = any(l.courses)
            join
                platforms pf on c.platform_from = pf.id
            join
                platforms pt on c.platform_to = pt.id
            join
                currencies cf on c.currency_from = cf.id
            join
                currencies ct on c.currency_to = ct.id
            group by
                l.id
        ) as ld
        """
    )


async def get_platforms():
    pool = await database_manager.get_pool()

    return await pool.fetch(
        """
        select
            name
        from
            platforms
        """
    )


async def get_currencies():
    pool = await database_manager.get_pool()

    return await pool.fetch(
        """
        select
            name
        from
            currencies
        """
    )
