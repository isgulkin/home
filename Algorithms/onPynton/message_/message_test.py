import unittest
from message import message


class MessageTest(unittest.TestCase):
    def test_1(self):
        self.assertEqual(message("80946"), 1)

    def test_2(self):
        self.assertEqual(message("21705"), 3)

    def test_3(self):
        self.assertEqual(message("33222"), 8)

    def test_4(self):
        self.assertEqual(message("0015278429"), 8)

    def test_5(self):
        self.assertEqual(message("3180232194"), 24)

    def test_6(self):
        self.assertEqual(message("2111223221"), 89)

    def test_7(self):
        self.assertEqual(message("6754734572886975459694519"), 4)

    def test_8(self):
        self.assertEqual(message("5082635579832836819403269"), 36)

    def test_9(self):
        self.assertEqual(message("3861332206123120110031010"), 3042)

    def test_10(self):
        self.assertEqual(message("3231311112121222122323111"), 121393)

    def test_11(self):
        self.assertEqual(
            message("66105415430540061635959290713250975704211395281440"), 3200
        )

    def test_12(self):
        self.assertEqual(
            message("31137622012253396063061840265383620210223721869311"), 194400
        )

    def test_13(self):
        self.assertEqual(
            message("33232122212133323231332331333221313332112312333222"), 20365011074
        )

    def test_14(self):
        self.assertEqual(
            message(
                "322191091222709462203225081001330301113202582212400823923887233298311602273"
            ),
            3833856000,
        )

    def test_15(self):
        self.assertEqual(
            message(
                "000222201233200252220320320132713330237136821100302035263810813100220203003"
            ),
            7188480000,
        )

    def test_16(self):
        self.assertEqual(
            message(
                "232113232332221312131312133223123232323132112323111132231311333333311223233"
            ),
            3416454622906707,
        )

    def test_17(self):
        self.assertEqual(
            message(
                "1317220535283308012096022025901126907092103322837090211312004139889680342020620082206039381214384122"
            ),
            2939328000,
        )

    def test_18(self):
        self.assertEqual(
            message(
                "7008011317323330131023207120250332012033901353523143008711141313076212221310202109091311023262012313"
            ),
            79073280000000,
        )

    def test_19(self):
        self.assertEqual(
            message(
                "2333221082021003312101100330033101232070710601332532201387331083012621123222739311113010213073512102"
            ),
            264648384000000,
        )

    def test_20(self):
        self.assertEqual(
            message(
                "1333313212132223121313233232232313232223121122223232332233113232212312322313232223111223222131121312"
            ),
            573147844013817084101,
        )


if __name__ == "__main__":
    unittest.main()
