import 'package:dio/dio.dart';

Future<String?> apiCurrency({required String path}) async {
  print("API CURRENCY");
  print(path);
  var dio = Dio(
    BaseOptions(
      connectTimeout: const Duration(seconds: 20),
      receiveTimeout: const Duration(seconds: 30),
      sendTimeout: const Duration(seconds: 20),
    ),
  );

  try {
    var formData = FormData();
    formData.files.add(
      MapEntry(
        "image",
        await MultipartFile.fromFile(path, filename: "pic-name.png"),
      ),
    );

    final response = await dio.post(
      "http://192.168.60.73:5000/currency",
      data: formData,
    );
    return response.data?.toString();
  } on DioException catch (e) {
    print("Dio error: ${e.message}");
  } catch (e) {
    print("Unexpected error: $e");
  }

  return null;
}
