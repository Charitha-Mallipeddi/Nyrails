# rm -f ./core/general/fixtures.json*
./manage.py dumpdata --format jsonl -o ./core/users/fixtures.jsonl.gz users.user
./manage.py dumpdata --format jsonl -o ./core/general/fixtures.jsonl.gz general
./manage.py dumpdata --format jsonl -o ./core/tariff/fixtures.jsonl.gz tariff.TicketType tariff.TicketTypeGroup tariff.SalesPackets tariff.SalesPacketsGroup

# ./manage.py dumpdata -o ./core/ticket/fixtures.json.gz --indent=2 ticket.tickettype ticket.ticketsource
# ./manage.py dumpdata -o ./core/mofa/fixtures.json.gz --indent=2 --database=mofa mofa
# general.Company \
# general.DeviceClass \
# general.DeviceClassGroup \
# general.Routes \
