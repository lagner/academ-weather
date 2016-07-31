#include <QGuiApplication>
#include <QQmlApplicationEngine>
#include <QQmlContext>
#include <QAbstractItemModel>
#include <QtQml>
#include <string>
#include <iostream>

using namespace std;

int main(int argc, char *argv[])
{
    QGuiApplication qtApp(argc, argv);
    QQmlApplicationEngine engine;

    engine.load(QUrl(QStringLiteral("qrc:/qml/main.qml")));

    return qtApp.exec();
}
