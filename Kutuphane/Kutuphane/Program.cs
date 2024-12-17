using System;
using OfficeOpenXml;
using System.Collections.Generic;
using System.IO;

internal class Program
{
    // Kitapları tutacak liste
    private static List<Kitap> kitaplar = new List<Kitap>();

    private static void Main(string[] args)
    {
        string excelDosyaYolu = "Kutuphane.xlsx";

        Console.WriteLine("Kütüphane Yönetim Sistemine Hoş Geldiniz!");

        while (true)
        {
            Console.WriteLine("\n1. Kitap Ekle");
            Console.WriteLine("2. Kitap Listele");
            Console.WriteLine("3. Çıkış");

            Console.Write("Seçiminizi yapın: ");
            string secim = Console.ReadLine() ?? string.Empty;

            switch (secim)
            {
                case "1":
                    KitapEkle();
                    ExcelDosyasinaKitapYaz(excelDosyaYolu);
                    break;
                case "2":
                    KitapListele();
                    break;
                case "3":
                    Console.WriteLine("Çıkış yapılıyor...");
                    return;
                default:
                    Console.WriteLine("Geçersiz bir seçim yaptınız.");
                    break;
            }
        }
    }

    private static void KitapEkle()
    {
        Console.WriteLine("\nKitap Ekleme İşlemi:");

        Console.Write("Kitap Adı: ");
        string ad = Console.ReadLine();

        Console.Write("Yazar: ");
        string yazar = Console.ReadLine();

        Console.Write("Yayın Yılı: ");
        int yayinYili = int.Parse(Console.ReadLine() ?? "0");

        Console.Write("Ödünç Durumu (Evet/Hayır): ");
        string oduncDurumu = Console.ReadLine();
        bool odunc = oduncDurumu?.ToLower() == "evet";

        int yeniID = kitaplar.Count > 0 ? kitaplar[^1].ID + 1 : 1;

        var yeniKitap = new Kitap
        {
            ID = yeniID,
            Ad = ad,
            Yazar = yazar,
            YayinYili = yayinYili,
            OduncDurumu = odunc
        };

        kitaplar.Add(yeniKitap);

        Console.WriteLine("Kitap başarıyla eklendi!");
    }

    private static void KitapListele()
    {
        Console.WriteLine("\nKitap Listesi:");

        if (kitaplar.Count == 0)
        {
            Console.WriteLine("Kütüphanede hiçbir kitap bulunmamaktadır.");
            return;
        }

        foreach (var kitap in kitaplar)
        {
            Console.WriteLine($"ID: {kitap.ID}, Ad: {kitap.Ad}, Yazar: {kitap.Yazar}, Yayın Yılı: {kitap.YayinYili}, Ödünç Durumu: {(kitap.OduncDurumu ? "Evet" : "Hayır")}");
        }
    }

    private static void ExcelDosyasinaKitapYaz(string dosyaYolu)
    {
        ExcelPackage.LicenseContext = LicenseContext.NonCommercial;

        using (var package = new ExcelPackage(new FileInfo(dosyaYolu)))
        {
            var worksheet = package.Workbook.Worksheets.Count == 0
                ? package.Workbook.Worksheets.Add("Kitaplar")
                : package.Workbook.Worksheets[0];

            // Başlıkları yaz
            worksheet.Cells[1, 1].Value = "ID";
            worksheet.Cells[1, 2].Value = "Kitap Adı";
            worksheet.Cells[1, 3].Value = "Yazar";
            worksheet.Cells[1, 4].Value = "Yayın Yılı";
            worksheet.Cells[1, 5].Value = "Ödünç Durumu";

            // Kitapları yaz
            int rowIndex = 2;
            foreach (var kitap in kitaplar)
            {
                worksheet.Cells[rowIndex, 1].Value = kitap.ID;
                worksheet.Cells[rowIndex, 2].Value = kitap.Ad;
                worksheet.Cells[rowIndex, 3].Value = kitap.Yazar;
                worksheet.Cells[rowIndex, 4].Value = kitap.YayinYili;
                worksheet.Cells[rowIndex, 5].Value = kitap.OduncDurumu ? "Evet" : "Hayır";
                rowIndex++;
            }

            package.Save();
        }
    }
}

// Kitap sınıfı
public class Kitap
{
    public int ID { get; set; }
    public string Ad { get; set; }
    public string Yazar { get; set; }
    public int YayinYili { get; set; }
    public bool OduncDurumu { get; set; }
}
