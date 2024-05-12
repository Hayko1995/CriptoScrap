import 'package:criptofront/request.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:flutter/widgets.dart';
import 'dart:async';

Timer? timer;

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Cripto',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.blue),
        useMaterial3: true,
      ),
      home: const MyHomePage(title: 'Cripto'),
    );
  }
}

class MyHomePage extends StatefulWidget {
  const MyHomePage({super.key, required this.title});

  final String title;

  @override
  State<MyHomePage> createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  late List<dynamic> coins = [];
  late List coinNames = [];
  late final List _coinNames = [];
  late bool openConfigs = false;
  late String selectedType = '';
  late String selectedCoin = '';
  late bool openPrices = false;
  late List<dynamic> results = [];
  late List<dynamic> _results = [];

  @override
  void dispose() {
    timer?.cancel();
    super.dispose();
  }

  getPrices(selectedCoin, selectedType) {
    String filter = '';
    results = [];
    if (selectedType == 'BORROW') {
      filter = "borrow";
    }
    if (selectedType == 'LEND') {
      filter = "deposit";
    }
    for (var item in coins) {
      if (item['name'] == selectedCoin) {
        var _item = {};
        _item['site'] = item['item'];
        _item['price'] = item[filter];
        _results.add(_item);
      }
    }
    setState(() {
      results = _results;
    });
  }

  Future<void> checkForNewSharedLists() async {
    MyAPI myAPi = MyAPI();
    List response = await myAPi.request();
    for (var item in coins) {
      if (!_coinNames.contains(item['name'])) {
        _coinNames.add(item['name']);
      }
    }

    setState(() {
      coins = response;
      coinNames = _coinNames;
    });
  }

  @override
  void initState() {
    checkForNewSharedLists();
    super.initState();
    timer = Timer.periodic(
        Duration(seconds: 5), (Timer t) => checkForNewSharedLists());
  }

  @override
  Widget build(BuildContext context) {
    if (coins.isEmpty) {
      checkForNewSharedLists();
    }
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
        title: Center(child: Text(widget.title)),
      ),
      body: Row(
        mainAxisAlignment: MainAxisAlignment.start,
        children: <Widget>[
          SizedBox(
            width: MediaQuery.sizeOf(context).width / 4,
            child: Row(
              mainAxisAlignment: MainAxisAlignment.start,
              children: [
                Column(
                  children: [
                    for (var item in coinNames)
                      Padding(
                        padding: const EdgeInsets.all(8.0),
                        child: SizedBox(
                          width: 100,
                          // height: 150,
                          child: ElevatedButton(
                              onPressed: () {
                                setState(() {
                                  openConfigs = true;
                                  openPrices = false;
                                  selectedCoin = item;
                                });
                              },
                              child: Text(item)),
                        ),
                      ),
                  ],
                ),
              ],
            ),
          ),
          Visibility(
            visible: openConfigs,
            child: Column(
              mainAxisAlignment: MainAxisAlignment.start,
              children: [
                for (var item in ['STAKING', 'LEND', "BORROW"])
                  SizedBox(
                    child: Padding(
                      padding: const EdgeInsets.fromLTRB(0, 8, 0, 0),
                      child: ElevatedButton(
                          onPressed: () {
                            setState(() {
                              openPrices = true;
                              selectedType = item;
                              getPrices(selectedCoin, selectedType);
                            });
                          },
                          child: Text(item)),
                    ),
                  ),
              ],
            ),
          ),
          Visibility(
            visible: openPrices,
            child: SizedBox(
              width: 400,
              child: Column(
                children: [
                  for (var item in results)
                    Padding(
                      padding: const EdgeInsets.fromLTRB(0, 8, 0, 0),
                      child: SizedBox(
                        width: 200,
                        child: ElevatedButton(
                            onPressed: () {}, child: Text(item.toString())),
                      ),
                    ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }
}
