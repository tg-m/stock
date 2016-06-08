#!/bin/bash

if [ $# -ne 1 ]; then
    echo "Usage:"
    echo "  $0 csv_with_gpw_stock_quotes"
    echo
    exit
fi

F=$1
SED="sed"

cat $F |\
$SED 's/,/./g' |\
$SED '1s/LP./lp/' |\
$SED '1s/Data/date/' |\
$SED '1s/Typ instrumentu/instrument_type/' |\
$SED '1s/Nazwa/name/' |\
$SED '1s/Kurs otwarcia/open/' |\
$SED '1s/Kurs maksymalny/high/' |\
$SED '1s/Kurs minimalny/low/' |\
$SED '1s/Kurs zamkniecia/close/' |\
$SED '1s/Zmiana/change/' |\
$SED '1s/Wolumen obrotu/volume/' |\
$SED '1s/Liczba transakcji/number_of_transactions/' |\
$SED '1s/Wartosc obrotu w tys. zl/exchange_value_in_thousands_of_pln/' |\
$SED '1s/Liczba otwartych pozycji/number_of_opened_positions/' |\
$SED '1s/Wartosc otwartych pozycji w mln zl/value_of_opened_positions_in_milions_of_pln/' |\
$SED '1s/Cena nominalna obligacji/nominal_price_of_obligation_bonds/' |\
$SED '1s/Waluta/currency/' >/tmp/gpw.temp.file;
cp /tmp/gpw.temp.file $F

