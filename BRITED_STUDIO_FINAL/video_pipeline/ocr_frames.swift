import AppKit
import Foundation
import Vision

var result: [String: String] = [:]
for argument in CommandLine.arguments.dropFirst() {
    let url = URL(fileURLWithPath: argument)
    guard let image = NSImage(contentsOf: url),
          let data = image.tiffRepresentation,
          let bitmap = NSBitmapImageRep(data: data),
          let cgImage = bitmap.cgImage else {
        result[argument] = ""
        continue
    }
    let request = VNRecognizeTextRequest()
    request.recognitionLevel = .accurate
    request.recognitionLanguages = ["fr-FR"]
    request.usesLanguageCorrection = true
    try? VNImageRequestHandler(cgImage: cgImage).perform([request])
    let text = (request.results ?? []).compactMap {
        $0.topCandidates(1).first?.string
    }.joined(separator: " ")
    result[argument] = text
}
let output = try! JSONSerialization.data(withJSONObject: result)
FileHandle.standardOutput.write(output)
