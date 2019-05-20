from sqlalchemy import or_
from sqlalchemy.dialects import postgresql
from models.Offer import Offer
from models.match import Match
from db import session


def main():
    try:
        offers: [Offer] = session.query(Offer).limit(10).all()
        for offer in offers:
            q = session.query(Offer) \
                .filter(or_(offer.newbuilding_id is None, Offer.newbuilding_id == offer.newbuilding_id),
                        or_(offer.bc_id is None, Offer.bc_id == offer.bc_id),
                        or_(offer.house_id is None, Offer.house_id == offer.house_id),
                        Offer.id != offer.id,
                        Offer.totalArea >= offer.totalArea-1,
                        Offer.totalArea <= offer.totalArea+1,
                        Offer.floorNumber >= offer.floorNumber-1,
                        Offer.floorNumber <= offer.floorNumber+1,
                        )
            # sql = q.statement.compile(dialect=postgresql.dialect(), compile_kwargs={"literal_binds": True})
            # print(sql)
            matches: [Offer] = q.all()
            for match in matches:
                session.merge(Match(offer.id, match.id))
            print("{} - {} matches".format(offer.id, matches.__len__()))
        session.commit()
    except Exception as e:
        print(e)
        print("Unknown exception..")
        exit()
    except KeyboardInterrupt:
        print("Finishing...")
        exit()
    print("Done.")


if __name__ == '__main__':
    main()
