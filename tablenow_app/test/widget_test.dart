// This is a basic Flutter widget test.
//
// To perform an interaction with a widget in your test, use the WidgetTester
// utility in the flutter_test package. For example, you can send tap and scroll
// gestures. You can also use WidgetTester to find child widgets in the widget
// tree, read text, and verify that the values of widget properties are correct.

import "package:flutter_test/flutter_test.dart";
import "package:supabase_flutter/supabase_flutter.dart";
import "package:tablenow_app/main.dart";

void main() {
  testWidgets("TableNow app renders", (WidgetTester tester) async {
    TestWidgetsFlutterBinding.ensureInitialized();
    await Supabase.initialize(
      url: "https://hnanftiymngdrnxcaxus.supabase.co",
      anonKey: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImhuYW5mdGl5bW5nZHJueGNheHVzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzUwNDc4MDAsImV4cCI6MjA5MDYyMzgwMH0.a8TGkK9Eyb_bor1QXzSXouHnTsWVbvnwPeciAkzaZDY",
    );
    await tester.pumpWidget(const TableNowApp());
    expect(find.text("TableNow"), findsOneWidget);
  });
}
