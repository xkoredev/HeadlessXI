using System;
using System.Net.Sockets;
using System.IO;
using System.Security.Cryptography;
using System.Threading;
using System.Net;
using System.IO.Compression;
using System.Diagnostics;
using System.Collections.Generic;
using System.Text;

namespace HeadlessFFXI
{
    class Program
    {
        public static Client User;
        static void Main(string[] args)
        {
            Config settings = new Config();
            settings.user = "admin";
            settings.password = "admin";
            settings.server = "localhost";
            settings.char_slot = 0;
            User = new Client(settings, false, true);
            User.Login();
            User.SendSay("Hello!");
            Thread.Sleep(15_000);
            User.SendSay("Goodbye!");
            User.Logout();
            Exit();
        }
        static void Exit()
        {
            System.Environment.Exit(1);
        }
    }
}
